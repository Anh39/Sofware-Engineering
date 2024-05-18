import { Button, Drawer, Dropdown } from "antd";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { DeleteSaved, getHistory, getSaved } from "../../Services/userService";
import { language } from "../../language";
import { ArrowRightOutlined, StarFilled } from "@ant-design/icons";
import "./drawer.css";

function Personal() {
    const [opensHistory, setOpenHistory] = useState(false);
    const [opensSaved, setOpenSaved] = useState(false);
    const [history, setHistory] = useState([]);
    const [savedText, setSavedText] = useState([]);

    const onHistory = () => {
        setOpenHistory(true);
    }

    const closeHistory = () => {
        setOpenHistory(false);
    }

    const onSaved = () => {
        setOpenSaved(true);
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

    const DeleteSave = async (id) => {
        console.log(id);
        const response = await DeleteSaved(id);
        if (response.ok) {
            setSavedText(savedText.filter(item => item.id === id));
        }
    }

    useEffect(() => {
        const fetchAPI = async () => {
            const response = await getHistory();
            if (response.ok) {
                const data = await response.json();
                setHistory(data);
            }

            const responseSaved = await getSaved();
            if (responseSaved.ok) {
                const dataSaved = await responseSaved.json();
                console.log(dataSaved);
                setSavedText(dataSaved);
            }
        }
        fetchAPI();
    }, [])

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
                    <div key={index} className="list">
                        <div>
                            <div>{language[value.from_language]} <ArrowRightOutlined /> {language[value.to_language]}</div>
                            <div>{value.from_content}</div>
                            <div>{value.to_content}</div>
                        </div>
                    </div>
                ))}
            </Drawer>

            <Drawer title="Bản dịch đã lưu" open={opensSaved} onClose={closeSaved} >
                {savedText.map((value, index) => (
                    <div key={index} className="list">
                        <div>
                            <div>{language[value.from_language]} <ArrowRightOutlined /> {language[value.to_language]}</div>
                            <div>{value.from_content}</div>
                            <div>{value.to_content}</div>
                        </div>
                        <div className="star" onClick={() => DeleteSave(index)}>
                            <StarFilled />
                        </div>
                    </div>
                ))}
            </Drawer>
        </>
    )
}

export default Personal;