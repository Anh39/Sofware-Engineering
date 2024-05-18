import { Button, Drawer, Dropdown } from "antd";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getHistory } from "../../Services/userService";

function Personal() {
    const [opensHistory, setOpenHistory] = useState(false);
    const [opensSaved, setOpenSaved] = useState(false);

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
            }
        }
        fetchAPI();
    }, [])

    return (
        <>
            <Dropdown
                menu={{items}}
                trigger={['click']}
            >
                <Button>
                    Personal
                </Button>
            </Dropdown>

            <Drawer title="lịch sử dịch" open={opensHistory} onClose={closeHistory} >
                <div>Bản dịch đã lưu</div>
                {
                    // bản dịch tại đây
                }
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