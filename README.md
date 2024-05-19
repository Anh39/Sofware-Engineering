# Phần mềm dịch 
## Thông tin nhóm phát triển :
Nhóm 39
Thành viên nhóm:
- [Vũ Đức Anh](https://github.com/Anh39 ) (22022514)
- [Dương Phương Hiểu](https://github.com/dphieu ) (22022659)
- [Trần Đức Hùng](https://github.com/hungtran1210 )(22022639)
## Demo :
- [Video cài đặt](https://drive.google.com/file/d/1CH6dNydhVpRW1qZ1qv9234KWv69HjDRz/view?usp=drive_link)
- [Video demo](https://drive.google.com/file/d/1QytFzMNVR26aRc83ousliNuHffiZYEz4/view?usp=drive_link)
- [Báo cáo](https://drive.google.com/file/d/1gCxazamSuBEfgTAChkbrx4rBqhbyy40C/view?usp=drive_link)
## Tính năng :
- Giao diện web.
- Dịch chữ từ nhiều ngôn ngữ sang cho nhau.
- Cho phép người dùng đăng ký tài khoảng và đăng nhập vào hệ thống.
- Lưu lịch sử dịch của người dùng.
- Người dùng có thể lưu lại một số bản dịch.
- Cho phép người dùng sử dụng backend dịch khác như Google Translate, Mymemory, ChatGPT (3.5 và 4).
## Công nghệ sử dụng:
- Backend : python [aiohttp](https://docs.aiohttp.org/en/stable/ ), [FastAPI](https://fastapi.tiangolo.com/)
- Server dịch : [MyMemory](https://mymemory.translated.net/), [Google Translate](https://translate.google.com/) thông qua [Playwright](https://playwright.dev/), [ChatGPT](https://platform.openai.com/docs/overview) thông qua [openai-python](https://github.com/openai/openai-python)
- Frontend: ReactJs, [ant.design](https://ant.design/)
- Database : [SQLAlchemy](https://www.sqlalchemy.org/)
## Đóng góp:
- Server backend : [Vũ Đức Anh](https://github.com/Anh39)
- Web frontend, ReactServer : [Dương Phương Hiểu](https://github.com/dphieu)
- Database : [Trần Đức Hùng](https://github.com/hungtran1210)
## Cài đặt
 - Chạy file install.bat
   - Nếu dịch dùng ChatGPT cần thêm file apikey.json vào theo đường dẫn backend\common\apikey.json với nội dung {"openai" : "api key của bạn"}
 - Chạy server bằng file main.py. trang web có thể truy cập bằng địa chỉ http://127.0.0.1:3000/
 - Chạy frontend bằng lệnh npm start
