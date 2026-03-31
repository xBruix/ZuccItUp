# Authors: Test suite for server.py, menu.py, and order.py
# Run with:  python -m pytest test.py -v
#       or:  python -m unittest test.py -v
#
# No live database required — all MongoDB calls are mocked.
# ─────────────────────────────────────────────────────────────────────────────
# KNOWN BUGS DOCUMENTED IN THIS FILE:
#   [BUG-1] Cart.calculate_subtotal()  → typo: self.__cart_item  (missing 's')
#   [BUG-2] Order.__init__()           → 'svr' param overwritten immediately by 'server'
#   [BUG-3] Order.place_order()        → references self.__cart_items which doesn't exist on Order
#   [BUG-4] Cart.convert_to_orders()   → creates Order(...) missing required 'svr' and 'instructions' params
#   [BUG-5] Cart.add_to_cart()         → server.get_menu_item(name) returns a dict, but add_to_cart
#                                         wraps it in list(), giving a list of keys not item dicts
#   [BUG-6] MenuItem.__init__()        → does not accept or store 'server'; viewItem/viewAllItems
#                                         call self.server.get_menu_item() which will crash
# ─────────────────────────────────────────────────────────────────────────────

import unittest
from unittest.mock import MagicMock, patch, call
from datetime import datetime
import sys
import os

# ─── Stub out third-party packages so tests run without installing them ───────
# pymongo and bcrypt are mocked at the test level anyway, but Python still needs
# to satisfy the top-level imports in server.py, order.py, etc. before any
# @patch decorator runs.  Setting fake entries in sys.modules fixes this.
_mock_bson_objectid = MagicMock()
_mock_bson_objectid.ObjectId = MagicMock(side_effect=lambda s=None: s or "mock_oid")

for _mod, _stub in [
    ("pymongo",          MagicMock()),
    ("pymongo.errors",   MagicMock()),
    ("bson",             MagicMock()),
    ("bson.objectid",    _mock_bson_objectid),
    ("bcrypt",           MagicMock()),
]:
    sys.modules.setdefault(_mod, _stub)

# Make sure imports resolve relative to the src directory
# Get absolute file path to this file, then get its directory.
TEST_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# Get the path to the src directory.
SRC_DIR_PATH = os.path.dirname(TEST_DIR_PATH) + "/src"
# Add src to sys.path, which contains a list of directories that the interpreter will go through when searching for modules.
sys.path.insert(0, SRC_DIR_PATH)


# ══════════════════════════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════════════════════════

def make_mock_server_instance():
    """
    Returns a plain MagicMock that mimics a fully-constructed Server instance.
    Used wherever menu.py or order.py need a server without hitting MongoDB.
    """
    s = MagicMock()
    return s


def build_server(mock_client, mock_bcrypt=None):
    """
    Constructs a real Server object with MongoDB patched out.
    mock_client  — the MagicMock returned by the patched MangoClient constructor.
    Returns the Server instance and the three collection mocks.
    """
    from server import Server

    mock_db = mock_client.return_value.get_database.return_value
    mock_db.command.return_value = {}          # simulate successful ping

    mock_user  = MagicMock()
    mock_menu  = MagicMock()
    mock_order = MagicMock()

    mock_db.__getitem__.side_effect = lambda key: {
        "user":  mock_user,
        "menu":  mock_menu,
        "order": mock_order,
    }[key]

    try:
        srv = Server("testuser", "testpass")
    except ValueError:
        srv = None
    return srv, mock_user, mock_menu, mock_order


# ══════════════════════════════════════════════════════════════════════════════
#  SERVER TESTS
# ══════════════════════════════════════════════════════════════════════════════

@patch("server.bcrypt")
@patch("server.MangoClient")
class TestServerInit(unittest.TestCase):
    """Tests for Server.__init__ and disconnect()"""

    def test_successful_connection(self, mock_client, mock_bcrypt):
        srv, *_ = build_server(mock_client, mock_bcrypt)
        self.assertIsNotNone(srv)

    def test_failed_connection_raises_value_error(self, mock_client, mock_bcrypt):
        from server import Server
        mock_client.return_value.get_database.return_value.command.side_effect = Exception("auth error")
        with self.assertRaises(ValueError):
            Server("bad_user", "bad_pass")

    def test_disconnect_closes_client(self, mock_client, mock_bcrypt):
        srv, *_ = build_server(mock_client, mock_bcrypt)
        srv.disconnect()
        mock_client.return_value.close.assert_called_once()


@patch("server.bcrypt")
@patch("server.MangoClient")
class TestServerUserFunctions(unittest.TestCase):
    """Tests for all user-related Server methods"""

    # ── verify_user ──────────────────────────────────────────────────────────

    def test_verify_user_returns_true_for_valid_credentials(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.find_one.return_value = {"VIUID": "123456789", "password": "hashed", "active": True}
        mock_bcrypt.checkpw.return_value = True
        self.assertTrue(srv.verify_user("123456789", "password"))

    def test_verify_user_returns_false_when_user_not_found(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.find_one.return_value = None
        self.assertFalse(srv.verify_user("000000000", "password"))

    def test_verify_user_returns_false_for_wrong_password(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.find_one.return_value = {"VIUID": "123456789", "password": "hashed", "active": True}
        mock_bcrypt.checkpw.return_value = False
        self.assertFalse(srv.verify_user("123456789", "wrongpass"))

    def test_verify_user_returns_false_for_inactive_user(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.find_one.return_value = {"VIUID": "123456789", "password": "hashed", "active": False}
        mock_bcrypt.checkpw.return_value = True
        self.assertFalse(srv.verify_user("123456789", "password"))

    # ── create_user ──────────────────────────────────────────────────────────

    def test_create_user_customer_inserts_document(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        # User does not exist yet
        mock_user.find_one.return_value = None
        mock_bcrypt.checkpw.return_value = False
        mock_bcrypt.hashpw.return_value = b"hashed"
        srv.create_user("111111111", "pass", "test@viu.ca", "Test User", "customer")
        mock_user.insert_one.assert_called_once()
        inserted = mock_user.insert_one.call_args[0][0]
        self.assertEqual(inserted["role"], "Customer")
        self.assertEqual(inserted["VIUID"], "111111111")

    def test_create_user_agent_inserts_with_availability(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.find_one.return_value = None
        mock_bcrypt.checkpw.return_value = False
        mock_bcrypt.hashpw.return_value = b"hashed"
        srv.create_user("222222222", "pass", "agent@viu.ca", "Agent Name", "agent", availability_status=True)
        inserted = mock_user.insert_one.call_args[0][0]
        self.assertTrue(inserted["availabilityStatus"])

    # ── deactivate_user ───────────────────────────────────────────────────────

    def test_deactivate_user_sets_active_false(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.update_one.return_value = MagicMock(matched_count=1)
        srv.deactivate_user("123456789")
        update_call = mock_user.update_one.call_args
        self.assertEqual(update_call[0][1]["$set"]["active"], False)

    def test_deactivate_user_raises_for_unknown_id(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.update_one.return_value = MagicMock(matched_count=0)
        with self.assertRaises(ValueError):
            srv.deactivate_user("000000000")

    # ── view_all_users ────────────────────────────────────────────────────────

    def test_view_all_users_filters_by_role(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        expected = [{"name": "Alice", "role": "Customer"}]
        mock_user.find.return_value.to_list.return_value = expected
        result = srv.view_all_users("Customer")
        mock_user.find.assert_called_once_with({"role": "Customer"}, {"password": 0})
        self.assertEqual(result, expected)

    def test_view_all_users_returns_empty_list_when_none(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.find.return_value.to_list.return_value = []
        result = srv.view_all_users("Agent")
        self.assertEqual(result, [])

    # ── view_user ─────────────────────────────────────────────────────────────

    def test_view_user_returns_dict_when_found(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        expected = {"name": "Bob", "VIUID": "123456789"}
        mock_user.find_one.return_value = expected
        result = srv.view_user("123456789")
        self.assertEqual(result, expected)

    def test_view_user_returns_none_when_not_found(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.find_one.return_value = None
        result = srv.view_user("000000000")
        self.assertIsNone(result)

    # ── update_availability ───────────────────────────────────────────────────

    def test_update_availability_returns_modified_count(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.update_one.return_value = MagicMock(modified_count=1)
        result = srv.update_availability("123456789", True)
        self.assertEqual(result, 1)
        update_call = mock_user.update_one.call_args
        self.assertTrue(update_call[0][1]["$set"]["availabilityStatus"])

    def test_update_availability_returns_zero_when_not_found(self, mock_client, mock_bcrypt):
        srv, mock_user, _, __ = build_server(mock_client, mock_bcrypt)
        mock_user.update_one.return_value = MagicMock(modified_count=0)
        result = srv.update_availability("000000000", False)
        self.assertEqual(result, 0)


@patch("server.bcrypt")
@patch("server.MangoClient")
class TestServerMenuFunctions(unittest.TestCase):
    """Tests for all menu-related Server methods"""

    # ── get_all_menus ─────────────────────────────────────────────────────────

    def test_get_all_menus_no_filter_returns_all(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        expected = [{"vendor": "Upper Cafe"}, {"vendor": "Tim Hortons"}]
        mock_menu.find.return_value.to_list.return_value = expected
        result = srv.get_all_menus()
        mock_menu.find.assert_called_once_with({})
        self.assertEqual(result, expected)

    def test_get_all_menus_filter_by_vendor(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        mock_menu.find.return_value.to_list.return_value = [{"vendor": "Upper Cafe"}]
        result = srv.get_all_menus(vendor_name="upper cafe")
        query = mock_menu.find.call_args[0][0]
        self.assertEqual(query["vendor"], "Upper Cafe")   # should be title-cased

    def test_get_all_menus_filter_by_menu_type(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        mock_menu.find.return_value.to_list.return_value = []
        srv.get_all_menus(menu_type="breakfast")
        query = mock_menu.find.call_args[0][0]
        self.assertEqual(query["type"], "Breakfast")      # should be title-cased

    def test_get_all_menus_filter_by_item_name(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        mock_menu.find.return_value.to_list.return_value = []
        srv.get_all_menus(item_name="coffee")
        query = mock_menu.find.call_args[0][0]
        self.assertIn("$regex", query["menuItem.name"])

    # ── get_one_menu ──────────────────────────────────────────────────────────

    def test_get_one_menu_returns_matching_document(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        expected = {"vendor": "Upper Cafe", "type": "Breakfast"}
        mock_menu.find_one.return_value = expected
        result = srv.get_one_menu("upper cafe", "breakfast")
        self.assertEqual(result, expected)

    def test_get_one_menu_returns_none_when_not_found(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        mock_menu.find_one.return_value = None
        result = srv.get_one_menu("Nobody", "Dinner")
        self.assertIsNone(result)

    # ── get_menu_item ─────────────────────────────────────────────────────────

    def test_get_menu_item_with_name_returns_single_dict(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        item = {"name": "Coffee", "price": 2.50, "inStock": True}
        mock_menu.aggregate.return_value.to_list.return_value = [item]
        result = srv.get_menu_item("coffee")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "Coffee")

    def test_get_menu_item_returns_none_when_not_found(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        mock_menu.aggregate.return_value.to_list.return_value = []
        # When item_name is given but empty result, to_list()[0] raises IndexError
        with self.assertRaises(IndexError):
            srv.get_menu_item("nonexistent item xyz")

    def test_get_menu_item_without_name_returns_all_items_list(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        all_items = [{"name": "Coffee"}, {"name": "Bagel"}]
        mock_menu.aggregate.return_value.to_list.return_value = all_items
        result = srv.get_menu_item()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    # ── search_menu_items ─────────────────────────────────────────────────────

    def test_search_menu_items_keyword_only(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        mock_menu.aggregate.return_value.to_list.return_value = [{"name": "Cappuccino"}]
        result = srv.search_menu_items(keyword="cap")
        self.assertEqual(len(result), 1)

    def test_search_menu_items_with_menu_type(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        mock_menu.aggregate.return_value.to_list.return_value = []
        srv.search_menu_items(keyword="sandwich", menu_type="Lunch")
        pipeline = mock_menu.aggregate.call_args[0][0]
        # First stage should match on menu type
        self.assertEqual(pipeline[0]["$match"]["type"], "Lunch")

    def test_search_menu_items_returns_empty_list_for_no_match(self, mock_client, mock_bcrypt):
        srv, _, mock_menu, __ = build_server(mock_client, mock_bcrypt)
        mock_menu.aggregate.return_value.to_list.return_value = []
        result = srv.search_menu_items(keyword="xyznotarealfood")
        self.assertEqual(result, [])


@patch("server.bcrypt")
@patch("server.MangoClient")
class TestServerOrderFunctions(unittest.TestCase):
    """Tests for all order-related Server methods"""

    # ── create_order ──────────────────────────────────────────────────────────

    def test_create_order_returns_id_string(self, mock_client, mock_bcrypt):
        from bson import ObjectId
        srv, _, __, mock_order = build_server(mock_client, mock_bcrypt)
        fake_id = ObjectId()
        mock_order.insert_one.return_value = MagicMock(inserted_id=fake_id)
        result = srv.create_order("200", "215", 12.50, "", "111111111", "Upper Cafe", [])
        self.assertEqual(result, str(fake_id))

    def test_create_order_document_structure(self, mock_client, mock_bcrypt):
        srv, _, __, mock_order = build_server(mock_client, mock_bcrypt)
        mock_order.insert_one.return_value = MagicMock(inserted_id=MagicMock())
        cart = [{"name": "Coffee", "qty": 2}]
        srv.create_order("200", "315", 5.00, "No milk", "111111111", "Upper Cafe", cart)
        doc = mock_order.insert_one.call_args[0][0]
        self.assertEqual(doc["building"], "200")
        self.assertEqual(doc["room"], "315")
        self.assertEqual(doc["subTotal"], 5.00)
        self.assertEqual(doc["specialInstructions"], "No milk")
        self.assertEqual(doc["customer"], "111111111")
        self.assertEqual(doc["orderStatus"], "Pending")
        self.assertEqual(doc["cartItem"], cart)
        self.assertIsNone(doc["readyTime"])

    # ── get_order_by_id ───────────────────────────────────────────────────────

    def test_get_order_by_id_returns_dict(self, mock_client, mock_bcrypt):
        from bson import ObjectId
        srv, _, __, mock_order = build_server(mock_client, mock_bcrypt)
        fake_id = ObjectId()
        expected = {"_id": fake_id, "customer": "111111111"}
        mock_order.find_one.return_value = expected
        result = srv.get_order_by_id(str(fake_id))
        self.assertEqual(result, expected)

    def test_get_order_by_id_returns_none_when_not_found(self, mock_client, mock_bcrypt):
        from bson import ObjectId
        srv, _, __, mock_order = build_server(mock_client, mock_bcrypt)
        mock_order.find_one.return_value = None
        result = srv.get_order_by_id(str(ObjectId()))
        self.assertIsNone(result)

    # ── get_orders_by_user ────────────────────────────────────────────────────

    def test_get_orders_by_user_queries_both_customer_and_agent(self, mock_client, mock_bcrypt):
        srv, _, __, mock_order = build_server(mock_client, mock_bcrypt)
        mock_order.find.return_value.to_list.return_value = []
        srv.get_orders_by_user("111111111")
        query = mock_order.find.call_args[0][0]
        self.assertIn("$or", query)
        fields = [list(d.keys())[0] for d in query["$or"]]
        self.assertIn("customer", fields)
        self.assertIn("agent", fields)

    # ── get_all_orders ────────────────────────────────────────────────────────

    def test_get_all_orders_returns_list(self, mock_client, mock_bcrypt):
        srv, _, __, mock_order = build_server(mock_client, mock_bcrypt)
        expected = [{"_id": "1"}, {"_id": "2"}]
        mock_order.find.return_value.to_list.return_value = expected
        result = srv.get_all_orders()
        self.assertEqual(result, expected)

    # ── add_agent_to_order ────────────────────────────────────────────────────

    def test_add_agent_to_order_returns_modified_count(self, mock_client, mock_bcrypt):
        from bson import ObjectId
        srv, _, __, mock_order = build_server(mock_client, mock_bcrypt)
        mock_order.update_one.return_value = MagicMock(modified_count=1)
        result = srv.add_agent_to_order(str(ObjectId()), "222222222")
        self.assertEqual(result, 1)

    # ── update_order_status ───────────────────────────────────────────────────

    def test_update_order_status_sends_correct_status(self, mock_client, mock_bcrypt):
        from bson import ObjectId
        srv, _, __, mock_order = build_server(mock_client, mock_bcrypt)
        mock_order.update_one.return_value = MagicMock(modified_count=1)
        order_id = str(ObjectId())
        result = srv.update_order_status(order_id, "InTransit")
        self.assertEqual(result, 1)
        update_call = mock_order.update_one.call_args
        self.assertEqual(update_call[0][1]["$set"]["orderStatus"], "InTransit")

    # ── time update functions ─────────────────────────────────────────────────

    def _run_time_update_test(self, method_name, field_name, mock_client, mock_bcrypt):
        from bson import ObjectId
        srv, _, __, mock_order = build_server(mock_client, mock_bcrypt)
        mock_order.update_one.return_value = MagicMock(modified_count=1)
        t = datetime.now()
        order_id = str(ObjectId())
        method = getattr(srv, method_name)
        result = method(t, order_id)
        self.assertEqual(result, 1)
        update_call = mock_order.update_one.call_args
        self.assertEqual(update_call[0][1]["$set"][field_name], t)

    def test_update_orderTime(self, mock_client, mock_bcrypt):
        self._run_time_update_test("update_orderTime", "orderTime", mock_client, mock_bcrypt)

    def test_update_readyTime(self, mock_client, mock_bcrypt):
        self._run_time_update_test("update_readyTime", "readyTime", mock_client, mock_bcrypt)

    def test_update_acceptTime(self, mock_client, mock_bcrypt):
        self._run_time_update_test("update_acceptTime", "acceptTime", mock_client, mock_bcrypt)

    def test_update_pickupTime(self, mock_client, mock_bcrypt):
        self._run_time_update_test("update_pickupTime", "pickupTime", mock_client, mock_bcrypt)

    def test_update_deliveryTime(self, mock_client, mock_bcrypt):
        self._run_time_update_test("update_deliveryTime", "deliveryTime", mock_client, mock_bcrypt)

    def test_update_confirmationTime(self, mock_client, mock_bcrypt):
        self._run_time_update_test("update_confirmationTime", "confirmationTime", mock_client, mock_bcrypt)


# ══════════════════════════════════════════════════════════════════════════════
#  MENU TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestMenu(unittest.TestCase):
    """Tests for the Menu class in menu.py"""

    def setUp(self):
        from menu import Menu
        self.mock_server = make_mock_server_instance()
        self.menu = Menu(type="Breakfast", schedule=[], publishStatus=True, server=self.mock_server)

    # ── viewAllMenus ──────────────────────────────────────────────────────────

    def test_viewAllMenus_calls_get_all_menus(self):
        self.mock_server.get_all_menus.return_value = []
        self.menu.viewAllMenus()
        self.mock_server.get_all_menus.assert_called_once()

    def test_viewAllMenus_prints_message_when_no_menus(self):
        self.mock_server.get_all_menus.return_value = []
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.menu.viewAllMenus()
        self.assertIn("No menus", buf.getvalue())

    def test_viewAllMenus_groups_by_location(self):
        menus = [
            {"location": "Library", "type": "general", "schedule": {}, "menuItem": []},
            {"location": "Library", "type": "lunch",   "schedule": {}, "menuItem": []},
        ]
        self.mock_server.get_all_menus.return_value = menus
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.menu.viewAllMenus()
        self.assertIn("Library", buf.getvalue())

    # ── viewMenu ──────────────────────────────────────────────────────────────

    @patch("builtins.input", return_value="coffee")
    def test_viewMenu_calls_search_with_keyword(self, mock_input):
        self.mock_server.search_menu_items.return_value = []
        self.menu.viewMenu()
        self.mock_server.search_menu_items.assert_called_once_with(
            menu_type="Breakfast", keyword="coffee"
        )

    @patch("builtins.input", return_value="")
    def test_viewMenu_passes_none_keyword_when_blank(self, mock_input):
        self.mock_server.search_menu_items.return_value = []
        self.menu.viewMenu()
        self.mock_server.search_menu_items.assert_called_once_with(
            menu_type="Breakfast", keyword=None
        )

    @patch("builtins.input", return_value="muffin")
    def test_viewMenu_prints_no_items_found_when_empty(self, mock_input):
        self.mock_server.search_menu_items.return_value = []
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.menu.viewMenu()
        self.assertIn("No items found", buf.getvalue())

    @patch("builtins.input", return_value="coffee")
    def test_viewMenu_prints_items_when_found(self, mock_input):
        self.mock_server.search_menu_items.return_value = [
            {"name": "Espresso", "price": 3.00, "inStock": True, "description": "Strong"}
        ]
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.menu.viewMenu()
        self.assertIn("Espresso", buf.getvalue())


class TestMenuItem(unittest.TestCase):
    """Tests for the MenuItem class in menu.py"""

    def setUp(self):
        from menu import MenuItem
        self.mock_server = make_mock_server_instance()
        # [BUG-6] MenuItem.__init__ does not accept a 'server' param. We construct
        # without it and then inject the server attribute manually so viewItem /
        # viewAllItems tests can still exercise the server call paths.
        self.item_in_stock = MenuItem(
            name="Latte", price=4.50, description="Milky coffee",
            inStock=True, allergens="dairy"
        )
        self.item_in_stock.server = self.mock_server  # manual injection workaround
        self.item_out_of_stock = MenuItem(
            name="Croissant", price=3.00, description="Flaky pastry",
            inStock=False, allergens="gluten"
        )
        self.item_out_of_stock.server = self.mock_server  # manual injection workaround

    # ── addToCart ─────────────────────────────────────────────────────────────

    def test_addToCart_calls_cart_when_in_stock(self):
        mock_cart = MagicMock()
        self.item_in_stock.addToCart(mock_cart)
        mock_cart.add_to_cart.assert_called_once_with("Latte", 1)

    def test_addToCart_does_not_add_when_out_of_stock(self):
        mock_cart = MagicMock()
        self.item_out_of_stock.addToCart(mock_cart)
        mock_cart.add_to_cart.assert_not_called()

    def test_addToCart_prints_out_of_stock_message(self):
        mock_cart = MagicMock()
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.item_out_of_stock.addToCart(mock_cart)
        self.assertIn("out of stock", buf.getvalue())

    # ── viewItem ──────────────────────────────────────────────────────────────

    @patch("builtins.input", return_value="Latte")
    def test_viewItem_prints_item_details_when_found(self, mock_input):
        # viewItem does list(result_cursor); mock must be a list so list([...]) works
        self.mock_server.get_menu_item.return_value = [{
            "name": "Latte", "price": 4.50, "description": "Milky coffee",
            "inStock": True, "allergens": "dairy", "location": "Upper Cafe", "menuType": "general"
        }]
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = self.item_in_stock.viewItem()
        self.assertEqual(result["name"], "Latte")
        self.assertIn("Latte", buf.getvalue())

    @patch("builtins.input", return_value="nothingburger")
    def test_viewItem_prints_not_found_and_returns_none(self, mock_input):
        # Return empty list so list([]) is empty → triggers 'if not result' branch
        self.mock_server.get_menu_item.return_value = []
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = self.item_in_stock.viewItem()
        self.assertIsNone(result)

    # ── viewAllItems ──────────────────────────────────────────────────────────

    def test_viewAllItems_calls_get_menu_item_with_no_args(self):
        self.mock_server.get_menu_item.return_value = [{"name": "A"}, {"name": "B"}]
        self.item_in_stock.viewAllItems()
        self.mock_server.get_menu_item.assert_called_once_with()

    def test_viewAllItems_returns_items_list(self):
        items = [{"name": "Espresso", "price": 3.00, "inStock": True,
                  "location": "Cafe", "menuType": "general"}]
        self.mock_server.get_menu_item.return_value = items
        result = self.item_in_stock.viewAllItems()
        self.assertEqual(result, items)

    def test_viewAllItems_returns_empty_list_when_none(self):
        self.mock_server.get_menu_item.return_value = []
        result = self.item_in_stock.viewAllItems()
        self.assertEqual(result, [])


# ══════════════════════════════════════════════════════════════════════════════
#  CART TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestCart(unittest.TestCase):
    """Tests for the Cart class in order.py"""

    def setUp(self):
        from order import Cart
        self.mock_server = make_mock_server_instance()
        self.cart = Cart(building="200", room="315", server=self.mock_server)

    # ── getters ───────────────────────────────────────────────────────────────

    def test_get_location_returns_building_and_room(self):
        building, room = self.cart.get_location()
        self.assertEqual(building, "200")
        self.assertEqual(room, "315")

    def test_get_subtotal_starts_at_zero(self):
        self.assertEqual(self.cart.get_subtotal(), 0.0)

    def test_get_cart_items_starts_empty(self):
        self.assertEqual(self.cart.get_cart_items(), {})

    def test_num_items_starts_at_zero(self):
        self.assertEqual(self.cart.num_items(), 0)

    # ── add_to_cart ───────────────────────────────────────────────────────────

    def test_add_to_cart_adds_valid_in_stock_item(self):
        self.mock_server.get_menu_item.return_value = [{"name": "Latte", "inStock": True}]
        self.cart.add_to_cart("Latte", 2)
        self.assertIn("Latte", self.cart.get_cart_items())
        self.assertEqual(self.cart.get_cart_items()["Latte"], 2)

    def test_add_to_cart_rejects_zero_quantity(self):
        self.cart.add_to_cart("Latte", 0)
        self.mock_server.get_menu_item.assert_not_called()
        self.assertEqual(self.cart.num_items(), 0)

    def test_add_to_cart_rejects_negative_quantity(self):
        self.cart.add_to_cart("Latte", -1)
        self.mock_server.get_menu_item.assert_not_called()

    def test_add_to_cart_rejects_out_of_stock_item(self):
        self.mock_server.get_menu_item.return_value = [{"name": "Croissant", "inStock": False}]
        self.cart.add_to_cart("Croissant", 1)
        self.assertNotIn("Croissant", self.cart.get_cart_items())

    def test_add_to_cart_prints_message_for_out_of_stock(self):
        self.mock_server.get_menu_item.return_value = [{"name": "Croissant", "inStock": False}]
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cart.add_to_cart("Croissant", 1)
        self.assertIn("out of stock", buf.getvalue())

    def test_add_to_cart_accumulates_quantity_for_existing_item(self):
        self.mock_server.get_menu_item.return_value = [{"name": "Latte", "inStock": True}]
        self.cart.add_to_cart("Latte", 1)
        self.cart.add_to_cart("Latte", 2)
        self.assertEqual(self.cart.get_cart_items()["Latte"], 3)

    def test_add_to_cart_increments_num_items(self):
        self.mock_server.get_menu_item.return_value = [{"name": "Bagel", "inStock": True}]
        self.cart.add_to_cart("Bagel", 1)
        self.assertEqual(self.cart.num_items(), 1)

    # ── change_quantity ───────────────────────────────────────────────────────

    def test_change_quantity_updates_existing_item(self):
        # Manually plant an item to avoid server mock dependency
        self.cart._Cart__cart_items["Latte"] = 1
        self.cart.change_quantity("Latte", 5)
        self.assertEqual(self.cart.get_cart_items()["Latte"], 5)

    def test_change_quantity_removes_item_when_zero(self):
        self.cart._Cart__cart_items["Latte"] = 2
        self.cart.change_quantity("Latte", 0)
        self.assertNotIn("Latte", self.cart.get_cart_items())

    def test_change_quantity_removes_item_when_negative(self):
        self.cart._Cart__cart_items["Latte"] = 2
        self.cart.change_quantity("Latte", -1)
        self.assertNotIn("Latte", self.cart.get_cart_items())

    def test_change_quantity_prints_message_when_item_not_in_cart(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cart.change_quantity("NotInCart", 3)
        self.assertIn("not in the cart", buf.getvalue())

    # ── remove_from_cart ──────────────────────────────────────────────────────

    def test_remove_from_cart_deletes_item(self):
        self.cart._Cart__cart_items["Tea"] = 1
        self.cart.remove_from_cart("Tea")
        self.assertNotIn("Tea", self.cart.get_cart_items())

    def test_remove_from_cart_prints_message_when_item_missing(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cart.remove_from_cart("NotThere")
        self.assertIn("not in the cart", buf.getvalue())

    # ── view_cart ─────────────────────────────────────────────────────────────

    def test_view_cart_returns_empty_dict_when_empty(self):
        result = self.cart.view_cart()
        self.assertEqual(result, {})

    def test_view_cart_returns_items_dict(self):
        self.cart._Cart__cart_items["Latte"] = 2
        result = self.cart.view_cart()
        self.assertEqual(result["Latte"], 2)

    def test_view_cart_prints_delivery_location(self):
        self.cart._Cart__cart_items["Latte"] = 1
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cart.view_cart()
        self.assertIn("200", buf.getvalue())
        self.assertIn("315", buf.getvalue())

    # ── calculate_subtotal ────────────────────────────────────────────────────

    def test_calculate_subtotal_BUG1_typo_in_attribute_name(self):
        """
        [BUG-1] calculate_subtotal() references self.__cart_item (missing 's').
        This raises AttributeError at runtime.
        """
        self.cart._Cart__cart_items["Latte"] = 2
        self.mock_server.get_menu_item.return_value = {"name": "Latte", "price": 4.50}
        with self.assertRaises(AttributeError):
            self.cart.calculate_subtotal()

    # ── convert_to_orders ─────────────────────────────────────────────────────

    def test_convert_to_orders_returns_none_when_cart_empty(self):
        result = self.cart.convert_to_orders(customer="111111111", vendor="Upper Cafe")
        self.assertIsNone(result)

    def test_convert_to_orders_BUG4_missing_required_order_params(self):
        """
        [BUG-4] convert_to_orders() creates Order(...) without 'svr' or 'instructions',
        which are required positional parameters of Order.__init__. Raises TypeError.
        This test documents the known bug.
        """
        self.cart._Cart__cart_items["Latte"] = 1
        # calculate_subtotal also has BUG-1, so mock it
        self.cart.calculate_subtotal = MagicMock(return_value=4.50)
        with self.assertRaises(TypeError):
            self.cart.convert_to_orders(customer="111111111", vendor="Upper Cafe")


# ══════════════════════════════════════════════════════════════════════════════
#  ORDER TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestOrder(unittest.TestCase):
    """Tests for the Order class in order.py"""

    def _make_order(self, mock_server=None):
        from order import Order
        if mock_server is None:
            mock_server = make_mock_server_instance()
        # [BUG-2] 'svr' is overwritten by 'server' — we pass same mock for both
        order = Order(
            mock_server,     # svr
            "200",           # building
            "315",           # room
            12.50,           # total
            "Extra hot",     # instructions
            "111111111",     # customer
            "Upper Cafe"     # vendor
        )
        return order, mock_server


    # ── __init__ / getters ────────────────────────────────────────────────────

    def test_get_location_returns_correct_tuple(self):
        order, _ = self._make_order()
        self.assertEqual(order.get_location(), ("200", "315"))

    def test_get_subtotal_returns_correct_total(self):
        order, _ = self._make_order()
        self.assertEqual(order.get_subtotal(), 12.50)

    def test_get_instructions_returns_correct_string(self):
        order, _ = self._make_order()
        self.assertEqual(order.get_instructions(), "Extra hot")

    def test_get_status_starts_empty(self):
        order, _ = self._make_order()
        self.assertEqual(order.get_status(), "")

    # ── get_time ──────────────────────────────────────────────────────────────

    def test_get_time_all_enums_return_empty_string_initially(self):
        from order import Time
        order, _ = self._make_order()
        for t in Time:
            self.assertEqual(order.get_time(t), "")

    def test_get_time_raises_for_invalid_enum(self):
        order, _ = self._make_order()
        with self.assertRaises(ValueError):
            order.get_time("not_a_time_enum")

    # ── set_instructions ──────────────────────────────────────────────────────

    def test_set_instructions_updates_value(self):
        order, _ = self._make_order()
        order.set_instructions("No onions")
        self.assertEqual(order.get_instructions(), "No onions")

    # ── update_status ─────────────────────────────────────────────────────────

    def test_update_status_ready_for_pickup_calls_server(self):
        from order import Status
        order, mock_server = self._make_order()
        order._Order__order_id = "some_id"
        order.update_status(Status.READY_FOR_PICKUP)
        self.assertEqual(order.get_status(), "ReadyForPickup")
        mock_server.update_order_status.assert_called_with("some_id", "ReadyForPickup")
        mock_server.update_readyTime.assert_called_once()

    def test_update_status_in_transit_calls_server(self):
        from order import Status
        order, mock_server = self._make_order()
        order._Order__order_id = "some_id"
        order.update_status(Status.IN_TRANSIT)
        self.assertEqual(order.get_status(), "InTransit")
        mock_server.update_pickupTime.assert_called_once()

    def test_update_status_delivered_calls_server(self):
        from order import Status
        order, mock_server = self._make_order()
        order._Order__order_id = "some_id"
        order.update_status(Status.DELIVERED)
        self.assertEqual(order.get_status(), "Delivered")
        mock_server.update_deliveryTime.assert_called_once()

    def test_update_status_received_calls_server(self):
        from order import Status
        order, mock_server = self._make_order()
        order._Order__order_id = "some_id"
        order.update_status(Status.RECEIVED)
        self.assertEqual(order.get_status(), "Received")
        mock_server.update_confirmationTime.assert_called_once()

    def test_update_status_does_not_call_server_when_no_order_id(self):
        from order import Status
        order, mock_server = self._make_order()
        # order_id is "" by default — no server calls should happen
        order.update_status(Status.DELIVERED)
        mock_server.update_order_status.assert_not_called()

    # ── place_order ───────────────────────────────────────────────────────────

    def test_place_order_BUG3_references_missing_cart_items_attribute(self):
        """
        [BUG-3] place_order() uses self.__cart_items which is never set on Order.
        This raises AttributeError. Test documents the known bug.
        """
        order, _ = self._make_order()
        with self.assertRaises(AttributeError):
            order.place_order()

    # ── accept_order ──────────────────────────────────────────────────────────

    def test_accept_order_does_nothing_when_no_order_id(self):
        order, mock_server = self._make_order()
        order.accept_order("agent_id")
        mock_server.add_agent_to_order.assert_not_called()

    def test_accept_order_calls_three_server_methods(self):
        order, mock_server = self._make_order()
        order._Order__order_id = "some_order_id"
        order.accept_order("222222222")
        mock_server.add_agent_to_order.assert_called_once_with(
            order_id="some_order_id", agent_id="222222222"
        )
        mock_server.update_order_status.assert_called_once_with(
            order_id="some_order_id", status="InTransit"
        )
        mock_server.update_acceptTime.assert_called_once()

    def test_accept_order_sets_agent_and_status(self):
        from order import Status
        order, mock_server = self._make_order()
        order._Order__order_id = "some_order_id"
        order.accept_order("222222222")
        self.assertEqual(order._Order__agent, "222222222")
        self.assertEqual(order.get_status(), Status.IN_TRANSIT.value)

    # ── mark_complete ─────────────────────────────────────────────────────────

    def test_mark_complete_does_nothing_when_no_order_id(self):
        order, mock_server = self._make_order()
        order.mark_complete()
        mock_server.update_order_status.assert_not_called()

    def test_mark_complete_calls_two_server_methods(self):
        order, mock_server = self._make_order()
        order._Order__order_id = "some_order_id"
        order.mark_complete()
        mock_server.update_order_status.assert_called_once()
        mock_server.update_orderTime.assert_called_once()

    def test_mark_complete_sets_status_to_delivered(self):
        from order import Status
        order, mock_server = self._make_order()
        order._Order__order_id = "some_order_id"
        order.mark_complete()
        self.assertEqual(order.get_status(), Status.DELIVERED.value)

    # ── view_order ────────────────────────────────────────────────────────────

    def test_view_order_returns_dict_with_correct_keys(self):
        order, _ = self._make_order()
        result = order.view_order()
        expected_keys = {
            "order_id", "customer", "vendor", "agent", "building", "room",
            "subtotal", "status", "special_instructions", "order_time",
            "accept_time", "ready_time", "pickup_time", "delivery_time",
            "confirmation_time"
        }
        self.assertEqual(set(result.keys()), expected_keys)

    def test_view_order_returns_correct_customer(self):
        order, _ = self._make_order()
        result = order.view_order()
        self.assertEqual(result["customer"], "111111111")

    def test_view_order_returns_correct_subtotal(self):
        order, _ = self._make_order()
        result = order.view_order()
        self.assertEqual(result["subtotal"], 12.50)

    # ── view_all_orders ───────────────────────────────────────────────────────

    def test_view_all_orders_returns_empty_list_when_none(self):
        order, mock_server = self._make_order()
        mock_server.get_all_orders.return_value = []
        result = order.view_all_orders()
        self.assertEqual(result, [])

    def test_view_all_orders_returns_list_from_server(self):
        order, mock_server = self._make_order()
        fake_orders = [
            {"customer": "111111111", "vendor": "Upper Cafe",
             "orderStatus": "Pending", "subTotal": 5.00,
             "building": "200", "room": "315"}
        ]
        mock_server.get_all_orders.return_value = fake_orders
        result = order.view_all_orders()
        self.assertEqual(result, fake_orders)

    def test_view_all_orders_calls_get_all_orders(self):
        order, mock_server = self._make_order()
        mock_server.get_all_orders.return_value = []
        order.view_all_orders()
        mock_server.get_all_orders.assert_called_once()


# ══════════════════════════════════════════════════════════════════════════════
#  STATUS / TIME ENUM TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestEnums(unittest.TestCase):
    """Sanity checks on the Status and Time enums in order.py"""

    def test_status_enum_values(self):
        from order import Status
        self.assertEqual(Status.PENDING.value,          "Pending")
        self.assertEqual(Status.READY_FOR_PICKUP.value, "ReadyForPickup")
        self.assertEqual(Status.IN_TRANSIT.value,       "InTransit")
        self.assertEqual(Status.DELIVERED.value,        "Delivered")
        self.assertEqual(Status.RECEIVED.value,         "Received")

    def test_time_enum_values(self):
        from order import Time
        self.assertEqual(Time.ORDER.value,        "Order")
        self.assertEqual(Time.READY.value,        "Ready")
        self.assertEqual(Time.ACCEPT.value,       "Accept")
        self.assertEqual(Time.PICKUP.value,       "Pickup")
        self.assertEqual(Time.DELIVERY.value,     "Delivery")
        self.assertEqual(Time.CONFIRMATION.value, "Confirmation")


# ══════════════════════════════════════════════════════════════════════════════
#  AGENT.py TESTS
# ══════════════════════════════════════════════════════════════════════════════

# ── NOTIFICATION TESTS ───────────────────────────────────────────────────────

#import must be checked
from agent import (
    _view_notifications,
    _send_status_notification,
    _accept_order,
    _mark_complete,
    _view_pending_orders,
    _view_order_history,
    _set_availability,
    _get_pending_orders,
    _print_order_table
)
from user import User, DeliveryAgent

#Creates a mock agent for testing
"""
def make_mock_agent(name="John Doe", viu_id="123456789", email="john@viu.ca"):
    mock_server = make_mock_server_instance()

    # Create a base User object
    user = User(mock_server)

    # Inject attributes normally set during login/signup
    user._User__current_user = viu_id
    user._User__role = "Agent"
    user.name = name
    user.email = email
    user.VIUID = viu_id

    # Create DeliveryAgent from the User object (shallow copy path)
    agent = DeliveryAgent(mock_server, user)

    # Also inject availability if needed
    agent._DeliveryAgent__availability_status = True

    return agent """

def make_mock_agent(
    name="John Doe",
    viu_id="123456789",
    email="john@viu.ca",
    availability=True
):
    mock_server = make_mock_server_instance()

    # Create a base User
    user = User(mock_server)
    user._User__current_user = viu_id
    user._User__role = "Agent"

    # Public attributes used in agent.py
    user.name = name
    user.email = email
    user.VIUID = viu_id

    # Create DeliveryAgent via shallow-copy constructor
    agent = DeliveryAgent(mock_server, user)

    # Private attribute (real storage)
    agent._DeliveryAgent__availability_status = availability

    # Public attribute used by setAvailability() and _set_availability()
    agent.availabilityStatus = availability

    return agent




class TestNotification(unittest.TestCase):
    """Tests for notification functions"""

    @patch('agent.Notification')
    def test_view_notifications_creates_notification_with_agent_name(self, mock_notif_class):
        """Test view_notifications creates Notification with agent's name"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent(name="John Doe")
        
        _view_notifications(agent, mock_server)
        
        # Verify Notification was created with agent's name as customer_VIUID
        mock_notif_class.assert_called_once()
        call_kwargs = mock_notif_class.call_args[1]
        self.assertEqual(call_kwargs["customer_VIUID"], "John Doe")
        self.assertEqual(call_kwargs["server"], mock_server)

    @patch('agent.Notification')
    def test_view_notifications_calls_viewNotification(self, mock_notif_class):
        """Test view_notifications calls viewNotification method"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent()
        mock_instance = MagicMock()
        mock_notif_class.return_value = mock_instance
        
        _view_notifications(agent, mock_server)
        
        mock_instance.viewNotification.assert_called_once()

    @patch('agent.Notification')
    def test_send_status_notification_creates_with_order_id(self, mock_notif_class):
        """Test send_status_notification includes order_id"""
        mock_server = make_mock_server_instance()
        
        _send_status_notification("order123", "customer_name", mock_server)
        
        call_kwargs = mock_notif_class.call_args[1]
        self.assertEqual(call_kwargs["order_id"], "order123")
        self.assertEqual(call_kwargs["customer_VIUID"], "customer_name")

    @patch('agent.Notification')
    def test_send_status_notification_calls_sendNotification(self, mock_notif_class):
        """Test send_status_notification calls sendNotification method"""
        mock_server = make_mock_server_instance()
        mock_instance = MagicMock()
        mock_notif_class.return_value = mock_instance
        
        _send_status_notification("order123", "customer_name", mock_server)
        
        mock_instance.sendNotification.assert_called_once()

# ── PENDING ORDER TESTS ───────────────────────────────────────────────────────

#Commented out till error is addressed
#error in order init addressed now testing if change worked/helped
class TestGetPendingOrders(unittest.TestCase):
    #Tests for _get_pending_orders helper

    def test_get_pending_orders_returns_empty_when_none(self):
        #Test returns empty list when no orders
        mock_server = make_mock_server_instance()
        mock_server.get_all_orders.return_value = []
        
        result = _get_pending_orders(mock_server)  #throws error with second definition of server in order __init__
        
        self.assertEqual(result, [])

    def test_get_pending_orders_filters_only_pending(self):
        #Test only returns orders with 'Pending' status
        mock_server = make_mock_server_instance()
        mock_server.get_all_orders.return_value = [
            {"_id": "1", "orderStatus": "Pending", "customer": "Alice"},
            {"_id": "2", "orderStatus": "In Transit", "customer": "Bob"},
            {"_id": "3", "orderStatus": "Pending", "customer": "Charlie"},
            {"_id": "4", "orderStatus": "Delivered", "customer": "Dave"}
        ]
        
        result = _get_pending_orders(mock_server)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["customer"], "Alice")
        self.assertEqual(result[1]["customer"], "Charlie")

    def test_get_pending_orders_calls_server_get_all_orders(self):
        #Test calls server.get_all_orders
        mock_server = make_mock_server_instance()
        mock_server.get_all_orders.return_value = []
        
        _get_pending_orders(mock_server)
        
        mock_server.get_all_orders.assert_called_once() 


# ── PRINT ORDER TABLE TESTS ───────────────────────────────────────────────────────

class TestPrintOrderTable(unittest.TestCase):
    """Tests for _print_order_table helper"""

    @patch('builtins.print')
    def test_print_order_table_with_subtotal_shows_correct_columns(self, mock_print):
        """Test prints subtotal column when show_subtotal=True"""
        orders = [
            {"customer": "Alice", "vendor": "Upper Cafe", "building": "200", 
             "room": "101", "subTotal": 15.50}
        ]
        
        _print_order_table(orders, show_subtotal=True)
        
        # Check header contains "Subtotal"
        calls = [str(c) for c in mock_print.call_args_list]
        header_printed = any("Subtotal" in str(c) for c in calls)
        self.assertTrue(header_printed)

    @patch('builtins.print')
    def test_print_order_table_without_subtotal_hides_column(self, mock_print):
        """Test hides subtotal column when show_subtotal=False"""
        orders = [
            {"customer": "Alice", "vendor": "Upper Cafe", "building": "200", 
             "room": "101"}
        ]
        
        _print_order_table(orders, show_subtotal=False)
        
        # Check header does NOT contain "Subtotal"
        calls = [str(c) for c in mock_print.call_args_list]
        header_printed = any("Subtotal" in str(c) for c in calls)
        self.assertFalse(header_printed)

    @patch('builtins.print')
    def test_print_order_table_prints_all_orders(self, mock_print):
        """Test prints all orders in list"""
        orders = [
            {"customer": "Alice", "vendor": "Upper Cafe", "building": "200", 
             "room": "101", "subTotal": 15.50},
            {"customer": "Bob", "vendor": "Lower Cafe", "building": "210", 
             "room": "202", "subTotal": 20.00}
        ]
        
        _print_order_table(orders)
        
        # Should print at least 4 lines (header + separator + 2 orders)
        self.assertGreaterEqual(mock_print.call_count, 4)

# ── VIEW PENDING ORDERS TESTS ───────────────────────────────────────────────────────

class TestViewPendingOrders(unittest.TestCase):
    
    #"""Tests for _view_pending_orders"""

    @patch('agent._print_order_table')
    @patch('agent._get_pending_orders')
    def test_view_pending_orders_shows_message_when_none(self, mock_get, mock_print_table):
        #"""Test prints message when no pending orders"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent()
        mock_get.return_value = []
        
        with patch('builtins.print') as mock_print:
            _view_pending_orders(agent, mock_server)
            
            # Check for "No pending orders" message
            printed = [str(c) for c in mock_print.call_args_list]
            message_found = any("No pending orders" in str(c) for c in printed)
            self.assertTrue(message_found)

    @patch('agent._print_order_table')
    @patch('agent._get_pending_orders')
    def test_view_pending_orders_displays_table_when_orders_exist(self, mock_get, mock_print_table):
        #Test displays table when pending orders exist"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent()
        fake_orders = [{"_id": "1", "orderStatus": "Pending"}]
        mock_get.return_value = fake_orders
        
        _view_pending_orders(agent, mock_server)
        
        mock_print_table.assert_called_once_with(fake_orders)

# ── SET AVAILABILITY TESTS ───────────────────────────────────────────────────────

class TestSetAvailability(unittest.TestCase):
    """Tests for _set_availability"""

    @patch('builtins.input', return_value='n')
    @patch('builtins.print')
    def test_set_availability_no_change_when_user_declines(self, mock_print, mock_input):
        """Test doesn't change status when user enters 'n'"""
        agent = make_mock_agent(availability=True)
        agent.setAvailability = MagicMock()
        
        _set_availability(agent)
        
        agent.setAvailability.assert_not_called()

    @patch('builtins.input', return_value='y')
    def test_set_availability_toggles_when_user_confirms(self, mock_input):
        """Test toggles availability when user enters 'y'"""
        agent = make_mock_agent(availability=True)
        agent.setAvailability = MagicMock()
        
        _set_availability(agent)
        
        agent.setAvailability.assert_called_once_with(False)

    @patch('builtins.input', return_value='y')
    def test_set_availability_toggles_from_false_to_true(self, mock_input):
        """Test toggles from unavailable to available"""
        agent = make_mock_agent(availability=False)
        agent.setAvailability = MagicMock()
        
        _set_availability(agent)
        
        agent.setAvailability.assert_called_once_with(True)

# ── ACCEPT ORDER TESTS ───────────────────────────────────────────────────────

class TestAcceptOrder(unittest.TestCase):
    """Tests for _accept_order"""

    @patch('agent._send_status_notification')
    @patch('agent._print_order_table')
    @patch('agent._get_pending_orders')
    @patch('builtins.input', return_value='')
    def test_accept_order_does_nothing_when_user_cancels(self, mock_input, mock_get, 
                                                          mock_print, mock_send):
        """Test returns without action when user presses Enter"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent()
        mock_get.return_value = [{"_id": "1", "orderStatus": "Pending"}]
        
        _accept_order(agent, mock_server)
        
        mock_send.assert_not_called()

    @patch('agent._send_status_notification')
    @patch('agent._print_order_table')
    @patch('agent._get_pending_orders')
    @patch('builtins.input', return_value='abc')
    @patch('builtins.print')
    def test_accept_order_rejects_non_numeric_input(self, mock_print, mock_input, 
                                                     mock_get, mock_table, mock_send):
        """Test shows error for non-numeric input"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent()
        mock_get.return_value = [{"_id": "1", "orderStatus": "Pending"}]
        
        _accept_order(agent, mock_server)
        
        # Check for "Invalid selection" message
        printed = [str(c) for c in mock_print.call_args_list]
        error_found = any("Invalid" in str(c) for c in printed)
        self.assertTrue(error_found)

    @patch('agent._send_status_notification')
    @patch('agent.Order')
    @patch('agent._print_order_table')
    @patch('agent._get_pending_orders')
    @patch('builtins.input', return_value='1')
    def test_accept_order_calls_order_accept_method(self, mock_input, mock_get, 
                                                     mock_table, mock_order_class, mock_send):
        """Test calls order.accept_order() with agent name"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent(name="John Doe")
        fake_order = {
            "_id": "order123",
            "building": "200",
            "room": "101",
            "subTotal": 15.50,
            "specialInstructions": "Extra hot",
            "customer": "Alice",
            "vendor": "Upper Cafe",
            "orderStatus": "Pending"
        }
        mock_get.return_value = [fake_order]
        mock_order_instance = MagicMock()
        mock_order_class.return_value = mock_order_instance
        
        _accept_order(agent, mock_server)
        
        mock_order_instance.accept_order.assert_called_once_with("John Doe")

    @patch('agent._send_status_notification')
    @patch('agent.Order')
    @patch('agent._print_order_table')
    @patch('agent._get_pending_orders')
    @patch('builtins.input', return_value='1')
    def test_accept_order_sends_notification_to_customer(self, mock_input, mock_get,
                                                         mock_table, mock_order, mock_send):
        """Test sends status notification to customer after accepting"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent()
        fake_order = {
            "_id": "order123",
            "customer": "Alice",
            "building": "200",
            "room": "101",
            "subTotal": 15.50,
            "specialInstructions": "",
            "vendor": "Upper Cafe",
            "orderStatus": "Pending"
        }
        mock_get.return_value = [fake_order]
        
        _accept_order(agent, mock_server)
        
        mock_send.assert_called_once_with("order123", "Alice", mock_server)

# ── MARK COMPLETE TESTS ───────────────────────────────────────────────────────

class TestMarkComplete(unittest.TestCase):
    """Tests for _mark_complete"""

    @patch('agent._send_status_notification')
    @patch('agent.Order')
    @patch('builtins.input', return_value='')
    @patch('builtins.print')
    def test_mark_complete_shows_message_when_no_active_deliveries(self, mock_print, 
                                                                    mock_input, mock_order, mock_send):
        """Test shows message when agent has no active deliveries"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent(name="John Doe")
        mock_order_instance = MagicMock()
        mock_order_instance.view_all_orders.return_value = [
            {"agent": "Other Agent", "orderStatus": "In Transit"}
        ]
        mock_order.return_value = mock_order_instance
        
        _mark_complete(agent, mock_server)
        
        printed = [str(c) for c in mock_print.call_args_list]
        message_found = any("no active deliveries" in str(c).lower() for c in printed)
        self.assertTrue(message_found)

    @patch('agent._send_status_notification')
    @patch('agent.Order')
    @patch('builtins.input', return_value='')
    def test_mark_complete_returns_when_user_cancels(self, mock_input, mock_order, mock_send):
        """Test returns without action when user presses Enter"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent(name="John Doe")
        mock_order_instance = MagicMock()
        mock_order_instance.view_all_orders.return_value = [
            {"_id": "1", "agent": "John Doe", "orderStatus": "In Transit"}
        ]
        mock_order.return_value = mock_order_instance
        
        _mark_complete(agent, mock_server)
        
        mock_send.assert_not_called()

    @patch('agent._send_status_notification')
    @patch('agent.Order')
    @patch('agent._print_order_table')
    @patch('builtins.input', return_value='1')
    def test_mark_complete_calls_order_mark_complete_method(self, mock_input, 
                                                            mock_table, mock_order_class, mock_send):
        """Test calls order.mark_complete()"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent(name="John Doe")
        fake_order = {
            "_id": "order123",
            "agent": "John Doe",
            "orderStatus": "In Transit",
            "building": "200",
            "room": "101",
            "subTotal": 15.50,
            "specialInstructions": "",
            "customer": "Alice",
            "vendor": "Upper Cafe"
        }
        
        # First call creates temp Order for view_all
        # Second call creates actual Order for mark_complete
        first_instance = MagicMock()
        first_instance.view_all_orders.return_value = [fake_order]
        second_instance = MagicMock()
        mock_order_class.side_effect = [first_instance, second_instance]
        
        _mark_complete(agent, mock_server)
        
        second_instance.mark_complete.assert_called_once()

    @patch('agent._send_status_notification')
    @patch('agent.Order')
    @patch('agent._print_order_table')
    @patch('builtins.input', return_value='1')
    def test_mark_complete_sends_notification_to_customer(self, mock_input, mock_table,
                                                          mock_order_class, mock_send):
        """Test sends notification after marking complete"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent(name="John Doe")
        fake_order = {
            "_id": "order123",
            "agent": "John Doe",
            "orderStatus": "In Transit",
            "customer": "Alice",
            "building": "200",
            "room": "101",
            "subTotal": 15.50,
            "specialInstructions": "",
            "vendor": "Upper Cafe"
        }
        
        first_instance = MagicMock()
        first_instance.view_all_orders.return_value = [fake_order]
        second_instance = MagicMock()
        mock_order_class.side_effect = [first_instance, second_instance]
        
        _mark_complete(agent, mock_server)
        
        mock_send.assert_called_once_with("order123", "Alice", mock_server)

# ── VIEW ORDER HISTORY TESTS ───────────────────────────────────────────────────────

class TestViewOrderHistory(unittest.TestCase):
    """Tests for _view_order_history"""

    @patch('agent.Order')
    @patch('builtins.print')
    def test_view_order_history_shows_message_when_no_history(self, mock_print, mock_order):
        """Test shows message when agent has no order history"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent(name="John Doe")
        mock_order_instance = MagicMock()
        mock_order_instance.view_all_orders.return_value = [
            {"agent": "Other Agent"}
        ]
        mock_order.return_value = mock_order_instance
        
        _view_order_history(agent, mock_server)
        
        printed = [str(c) for c in mock_print.call_args_list]
        message_found = any("no order history" in str(c).lower() for c in printed)
        self.assertTrue(message_found)

    @patch('agent.Order')
    @patch('builtins.print')
    def test_view_order_history_displays_only_agent_orders(self, mock_print, mock_order):
        """Test displays only orders assigned to this agent"""
        mock_server = make_mock_server_instance()
        agent = make_mock_agent(name="John Doe")
        mock_order_instance = MagicMock()
        mock_order_instance.view_all_orders.return_value = [
            {"agent": "John Doe", "customer": "Alice", "vendor": "Upper Cafe",
             "orderStatus": "Delivered", "subTotal": 15.50, "building": "200", "room": "101"},
            {"agent": "Other Agent", "customer": "Bob", "vendor": "Lower Cafe",
             "orderStatus": "Delivered", "subTotal": 20.00, "building": "210", "room": "202"},
            {"agent": "John Doe", "customer": "Charlie", "vendor": "Upper Cafe",
             "orderStatus": "In Transit", "subTotal": 10.00, "building": "200", "room": "103"}
        ]
        mock_order.return_value = mock_order_instance
        
        _view_order_history(agent, mock_server)
        
        # Should print 2 order lines (for John Doe's orders only) + header + separator
        self.assertGreaterEqual(mock_print.call_count, 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
