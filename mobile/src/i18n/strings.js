/**
 * Every text the app shows, one dictionary per language (US11). English and Vietnamese come first.
 *
 * English is the default and the reference: it matches the acceptance criteria word for word, and
 * every other dictionary must have exactly its keys, or the tests fail. A new screen adds its keys
 * to every dictionary. A new language is one more dictionary with every key translated; the
 * language switch lists it with no other change.
 * Notes and amounts the user types are data, not text, and are never translated.
 */

export const strings = {
  en: {
    'app.title': 'Personal Expense Management App',

    'login.title': 'Sign in',
    'login.subtitle': 'Sign in to see your recent entries.',
    'login.email': 'Email',
    'login.password': 'Password',
    'login.submit': 'Sign in',
    'login.missing': 'Enter your email and password',

    'overview.title': 'Recent entries',
    'overview.count': 'The {shown} most recent of {total} entries',
    'overview.refresh': 'Refresh',
    'overview.refreshing': 'Refreshing…',
    'overview.signOut': 'Sign out',
    'overview.empty': 'No entries yet.',
    'overview.noConnection': 'No connection. Tap Refresh to try again',

    'entry.noNote': 'No note',
    'entry.noKind': 'No kind of spending',

    'error.incorrectSignIn': 'Incorrect email or password',
    'error.signInAgain': 'Please sign in again',
    'error.cannotReach': 'Cannot reach the server at {url}',
    'error.server': 'Server error ({status})',

    'category.Food': 'Food',
    'category.Transport': 'Transport',
    'category.Shopping': 'Shopping',
    'category.Bills': 'Bills',
    'category.Entertainment': 'Entertainment',
    'category.Health': 'Health',
    'category.Education': 'Education',
    'category.Other': 'Other',
    'category.Salary': 'Salary',
    'category.Bonus': 'Bonus',
    'category.Other income': 'Other income',

    'language.switch': 'Language',
    'language.name': 'English',

    // How the language groups thousands: 55,000 ₫ in English, as docs/requirements.md writes it.
    'number.thousands': ',',
  },

  vi: {
    'app.title': 'Ứng dụng quản lý chi tiêu cá nhân',

    'login.title': 'Đăng nhập',
    'login.subtitle': 'Đăng nhập để xem các khoản thu chi gần đây.',
    'login.email': 'Email',
    'login.password': 'Mật khẩu',
    'login.submit': 'Đăng nhập',
    'login.missing': 'Hãy nhập email và mật khẩu',

    'overview.title': 'Giao dịch gần đây',
    'overview.count': '{shown} giao dịch gần nhất trong tổng số {total}',
    'overview.refresh': 'Làm mới',
    'overview.refreshing': 'Đang làm mới…',
    'overview.signOut': 'Đăng xuất',
    'overview.empty': 'Chưa có giao dịch nào.',
    'overview.noConnection': 'Không có mạng. Bấm Làm mới để thử lại',

    'entry.noNote': 'Không có ghi chú',
    'entry.noKind': 'Chưa chọn loại chi tiêu',

    'error.incorrectSignIn': 'Email hoặc mật khẩu không đúng',
    'error.signInAgain': 'Vui lòng đăng nhập lại',
    'error.cannotReach': 'Không kết nối được máy chủ tại {url}',
    'error.server': 'Lỗi máy chủ ({status})',

    'category.Food': 'Ăn uống',
    'category.Transport': 'Đi lại',
    'category.Shopping': 'Mua sắm',
    'category.Bills': 'Hóa đơn',
    'category.Entertainment': 'Giải trí',
    'category.Health': 'Sức khỏe',
    'category.Education': 'Giáo dục',
    'category.Other': 'Chi khác',
    'category.Salary': 'Lương',
    'category.Bonus': 'Thưởng',
    'category.Other income': 'Thu nhập khác',

    'language.switch': 'Ngôn ngữ',
    'language.name': 'Tiếng Việt',

    'number.thousands': '.',
  },
};
