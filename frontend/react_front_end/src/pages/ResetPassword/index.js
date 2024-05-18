import { Button, Card, Col, Form, Input, Row, message } from "antd";
import { ChangePassword } from "../../Services/userService";
import { useNavigate } from "react-router-dom";

function ResetPassword() {
    const navigate = useNavigate();
    const rules = [
        {
            required: true,
            message: 'Bắt buộc!'
        }
    ];

    const onFinish = async (e) => {
        console.log(e);

        if (e.newPassword !== e.repeateNewPassword) {
            message.error("Mật khẩu mới và viết lại mật khẩu mới không khớp");
            return;
        }

        const options = {
            old_password: e.oldPassword,
            new_password:  e.newPassword
        }

        const response = await ChangePassword(options);

        if (response.ok) {
            message.success("Đặt lại mật khẩu thành công");
            navigate("/");
        } else {
            message.error("Đặt lại mật khẩu thất bại");
        }
    }
    return (
        <>
            <Row justify="center">
                <Col span={12}>
                    <Card title="Đặt lại mật khẩu">
                        <Form onFinish={onFinish}>
                            <Form.Item label="Mật khẩu cũ" name="oldPassword" rules={rules} >
                                <Input.Password />
                            </Form.Item>
                            <Form.Item label="Mật khẩu mới" name="newPassword" rules={rules} >
                                <Input.Password />
                            </Form.Item>
                            <Form.Item label="Viết lại mật khẩu mới" name="repeateNewPassword" rules={rules} >
                                <Input.Password />
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit">
                                    Đặt lại mật khẩu
                                </Button>
                            </Form.Item>
                        </Form>
                    </Card>
                </Col>
            </Row>
        </>
    )
}

export default ResetPassword;