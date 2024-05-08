import { Button, Drawer } from "antd";
import { useState } from "react";
import { Link } from "react-router-dom";

// Laptop gaming, đồ họa

function Header(props) {
    const { token } = props;

    const [open, setOpen] = useState(false);

    const showDrawer = () => {
        setOpen(true);
    };

    const onClose = () => {
        setOpen(false);
    };

    return (
        <>
            <div className="header">
                <div className="header__logo">
                    <Link to="/">Translator</Link>
                </div>

                <div className="header__button">
                    {token ? (
                        <>
                            <Button className="header__button--login" type="primary" onClick={showDrawer}>
                                bản dịch đã lưu
                            </Button>
                            <Button className="header__button--register">
                                <Link to="/logout">Đăng xuất</Link>
                            </Button>
                        </>
                    ) : (
                        <>
                            <Button className="header__button--login" type="primary">
                                <Link to="/login">Đăng nhập</Link>
                            </Button>
                            <Button className="header__button--register">
                                <Link to="/register">Đăng kí</Link>
                            </Button>
                        </>
                    )}
                </div>
            </div>

            <Drawer title="Bản dịch đã lưu" onClose={onClose} open={open}>
                <p>Nothing</p>
            </Drawer>
        </>
    )
}

export default Header;