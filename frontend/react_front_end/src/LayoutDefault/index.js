import { Layout } from "antd";
import "./LayoutDefault.css";
import Header from "./Header";
import Footer from "./Footer";
import Main from "./Main";

function LayoutDefault() {
    

    return (
        <>
            <Layout className="layout-default">
                <Header />
                <div className="below-header">
                    <Main />
                    <Footer />
                </div>
            </Layout>
        </>
    )
}

export default LayoutDefault;