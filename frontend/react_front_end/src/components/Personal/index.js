import { Button, Drawer, Dropdown } from "antd";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getHistory, getSaved } from "../../Services/userService";
import { language } from "../../language";
import { ArrowRightOutlined } from "@ant-design/icons";
import "./drawer.css";

function Personal() {
    const [opensHistory, setOpenHistory] = useState(false);
    const [opensSaved, setOpenSaved] = useState(false);
    const [history, setHistory] = useState([]);

    const onHistory = () => {
        setOpenHistory(true);
    }

    const closeHistory = () => {
        setOpenHistory(false);
    }

    const onSaved = () => {
        setOpenHistory(true);
    }

    const closeSaved = () => {
        setOpenSaved(false);
    }

    const items = [
        {
            key: 'history',
            label: <div onClick={onHistory}>Lịch sử dịch</div>
        },
        {
            key: 'saved',
            label: <div onClick={onSaved}>Bản dịch đã lưu</div>
        },
        {
            key: 'resetpassword',
            label: <Link to="/resetpassword">Đổi mật khẩu</Link>
        },
        {
            key: 'logout',
            label: <Link to="/logout">Đăng xuất</Link>
        }
    ];

    useEffect(() => {
        const fetchAPI = async () => {
            const response = await getHistory();
            if (response.ok) {
                const data = await response.json();
                console.log(data);
                setHistory(data);
            }
        }
        fetchAPI();
    }, [])

    history.map((value, index) => {
        console.log(value);
    })

    return (
        <>
            <Dropdown
                menu={{ items }}
                trigger={['click']}
            >
                <Button>
                    Personal
                </Button>
            </Dropdown>

            <Drawer title="lịch sử dịch" open={opensHistory} onClose={closeHistory} >
                {history.map((value, index) => (
                    <div key={index} className="history">
                        <div>
                            {language[value.from_language]} <ArrowRightOutlined /> {language[value.to_language]}
                        </div>
                        <div>
                            {value.from_content}
                        </div>
                        <div>
                            {value.to_content}
                        </div>
                    </div>
                ))}
            </Drawer>

            <Drawer title="Bản dịch đã lưu" open={opensSaved} onClose={closeSaved} >
                <div>Bản dịch đã lưu</div>
                {
                    // bản dịch tại đây
                }
            </Drawer>
        </>
    )
}

export default Personal;