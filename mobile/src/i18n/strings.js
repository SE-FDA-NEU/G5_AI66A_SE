/**
 * Every text the app shows, one dictionary per language (US11). English and Vietnamese come first.
 *
 * English is the default and the reference: it matches the acceptance criteria word for word, and
 * every other dictionary must have exactly its keys, or the tests fail. A new screen adds its keys
 * to every dictionary. A new language is one more dictionary with every key translated; the
 * language switch lists it with no other change.
 * Notes and amounts the user types are data, not text, and are never translated.
 *
 * An error has a message, the exact sentence of the acceptance criteria, and may have a hint under
 * the same key plus ".hint": why it happened and what to do next (docs/ui.md, section 3).
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
    'error.incorrectSignIn.hint': 'Check both and try again.',
    'error.signInAgain': 'Please sign in again',
    'error.signInAgain.hint': 'A sign-in lasts 7 days, and yours has ended.',
    'error.emailTaken': 'This email is already registered',
    'error.emailTaken.hint': 'Sign in with it instead, or create the account with another address.',
    'error.passwordLength': 'Password must be 6 to 128 characters',
    'error.passwordLength.hint': 'One under 6 characters is too easy to guess. Choose one of 6 to 128 characters and try again.',
    'error.invalidEmail': 'Enter a valid email address',
    'error.invalidEmail.hint': 'An address looks like name@example.com.',
    'error.amountNotPositive': 'Enter an amount greater than 0',
    'error.amountNotPositive.hint': 'Write it in whole dong, such as 55000. Nothing was saved.',
    'error.dateInFuture': 'The date cannot be in the future',
    'error.dateInFuture.hint': 'An entry records money already spent or received, so choose today or an earlier day. Nothing was saved.',
    'error.unknownCategory': 'Choose a kind of spending from the list',
    'error.unknownCategory.hint': 'Tap one of the kinds shown, or none at all. Nothing was saved.',
    'error.invalidMonth': 'Month must be written YYYY-MM',
    'error.invalidMonth.hint': 'Reload the page: the app asks for this month by itself.',
    'error.invalidRequest': 'The server could not read what the app sent',
    'error.invalidRequest.hint': 'Nothing was saved. Reload the page and try again; if it happens again, tell the team what you typed.',
    'error.notFound': 'The server does not offer this yet',
    'error.notFound.hint': 'The app is newer than the backend. Pull the latest main, then restart the backend.',
    'error.cannotReach': 'Cannot reach the server at {url}',
    'error.cannotReach.hint': 'Check that the backend is running (docs/SETUP.md, section 4), then try again.',
    'error.server': 'The server could not finish this request',
    'error.server.hint': 'Try again in a moment. If it keeps happening, the backend terminal shows what went wrong.',
    'error.refused': 'The server refused this request',
    'error.refused.hint': 'Try again. If it happens again, tell the team what you did.',

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
    'error.incorrectSignIn.hint': 'Hãy kiểm tra cả hai rồi thử lại.',
    'error.signInAgain': 'Vui lòng đăng nhập lại',
    'error.signInAgain.hint': 'Mỗi lần đăng nhập dùng được 7 ngày, và lần của bạn đã hết hạn.',
    'error.emailTaken': 'Email này đã được đăng ký',
    'error.emailTaken.hint': 'Hãy đăng nhập bằng email này, hoặc tạo tài khoản bằng địa chỉ khác.',
    'error.passwordLength': 'Mật khẩu phải từ 6 đến 128 ký tự',
    'error.passwordLength.hint': 'Mật khẩu dưới 6 ký tự rất dễ bị đoán. Hãy chọn mật khẩu từ 6 đến 128 ký tự rồi thử lại.',
    'error.invalidEmail': 'Hãy nhập một địa chỉ email hợp lệ',
    'error.invalidEmail.hint': 'Địa chỉ email có dạng ten@example.com.',
    'error.amountNotPositive': 'Hãy nhập số tiền lớn hơn 0',
    'error.amountNotPositive.hint': 'Ghi số đồng chẵn, ví dụ 55000. Chưa có gì được lưu.',
    'error.dateInFuture': 'Ngày không được ở tương lai',
    'error.dateInFuture.hint': 'Mỗi giao dịch ghi lại tiền đã chi hoặc đã nhận, nên hãy chọn hôm nay hoặc một ngày trước đó. Chưa có gì được lưu.',
    'error.unknownCategory': 'Hãy chọn loại chi tiêu trong danh sách',
    'error.unknownCategory.hint': 'Bấm chọn một loại có sẵn, hoặc không chọn loại nào. Chưa có gì được lưu.',
    'error.invalidMonth': 'Tháng phải được ghi theo dạng YYYY-MM',
    'error.invalidMonth.hint': 'Hãy tải lại trang: app tự hỏi tháng hiện tại.',
    'error.invalidRequest': 'Máy chủ không đọc được dữ liệu app gửi',
    'error.invalidRequest.hint': 'Chưa có gì được lưu. Hãy tải lại trang rồi thử lại; nếu vẫn lỗi, báo nhóm bạn đã nhập gì.',
    'error.notFound': 'Máy chủ chưa có chức năng này',
    'error.notFound.hint': 'App mới hơn backend. Hãy lấy bản main mới nhất rồi khởi động lại backend.',
    'error.cannotReach': 'Không kết nối được máy chủ tại {url}',
    'error.cannotReach.hint': 'Hãy kiểm tra backend đang chạy (docs/SETUP.md, mục 4), rồi thử lại.',
    'error.server': 'Máy chủ không hoàn tất được yêu cầu này',
    'error.server.hint': 'Hãy thử lại sau giây lát. Nếu vẫn lỗi, cửa sổ terminal của backend cho biết lỗi gì.',
    'error.refused': 'Máy chủ từ chối yêu cầu này',
    'error.refused.hint': 'Hãy thử lại. Nếu vẫn bị từ chối, báo nhóm bạn đã làm gì.',

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
