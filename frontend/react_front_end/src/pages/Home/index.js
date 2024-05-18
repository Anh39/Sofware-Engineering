import { Button, Col, Flex, Row, Select } from "antd";
import { ZhihuOutlined, PaperClipOutlined, SwapOutlined, SoundOutlined, CopyOutlined, StarOutlined, StarFilled } from "@ant-design/icons";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../../language";
import { language } from "../../language";
import TextArea from "antd/es/input/TextArea";
import { getCookie, setCookie } from "../../helpers/cookie";
import { translateTextServer,entry} from "../../Services/userService";

async function init() {
    const response = await entry();
    const data = await response.json();
    if (data.success === true) {
        // setCookie("id", data.id, 1);
        // setCookie("username", data.username, 1);
        // setCookie("email", data.email, 1);
        setCookie("token", data.token, {path:'/'});
        //document.cookie = `token=${data.token};path=/;`
    } else {
        console.log('Entry Error');
    }
}

await init();

function Home() {
    const token = getCookie("token");

    const [FromLang, setFromLang] = useState({ value: 'en-GB', label: language['en-GB'] });
    const [ToLang, setToLang] = useState({ value: 'vi-VN', label: language['vi-VN'] });

    const [inputText, setInputText] = useState('');
    const [translatedText, setTranslatedText] = useState('');

    const languageOptions = Object.keys(language).map((key) => ({
        label: language[key],
        value: key,
    }));

    const [selectedButton, setSelectedButton] = useState("");
    const [isSaved, setIsSaved] = useState(false);

    const handleClick = (buttonType) => {
        setSelectedButton(buttonType);
    }

    const translateText = async (text) => {
        // const apiUrl = `https://api.mymemory.translated.net/get?q=${text}&langpair=${FromLang.label}|${ToLang.label}`;
        // const response = await fetch(apiUrl);
        // const data = await response.json();
        // if (data.responseData) {
        //     setTranslatedText(data.responseData.translatedText);
        // }
        // const apiUrl = `https://api.mymemory.translated.net/get?q=${text}&langpair=${FromLang.label}|${ToLang.label}`;
        let mapping = {
            'English' : 'en-GB',
            'Vietnamese' : 'vi-VN'
        }
        const options = {
            from_language : mapping[FromLang.label],
            to_language : mapping[ToLang.label],
            from_content : text,
            engine : 'auto'
        }
        console.log('Cookie : ',document.cookie);
        const response = await translateTextServer(options);
        if (response.ok) {
            const data = await response.json();
            setTranslatedText(data.to_content);
        } else {
            try {
                setTranslatedText(response.text());
            }
            catch {
                setTranslatedText('Exception');
            }
        }

    };

    const SwapLang = () => {
        let temp = FromLang;
        setFromLang(ToLang);
        setToLang(temp);

        let tempText = inputText;
        setInputText(translatedText);
        setTranslatedText(tempText);
    }

    const handleChangeFromLang = (label, value) => {
        console.log(label, value);
        setFromLang({ value: label, label: value });
    }

    const handleChangeToLang = (value, option) => {
        console.log(value, option);
        setToLang({ value: option, label: option });
    }

    const SpeakInputText = () => {
        const synth = window.speechSynthesis;
        const utterThis = new SpeechSynthesisUtterance(inputText);
        utterThis.lang = FromLang.label;
        synth.speak(utterThis);
    }

    const SpeakTranslatedText = () => {
        const synth = window.speechSynthesis;
        const utterThis = new SpeechSynthesisUtterance(translatedText);
        utterThis.lang = ToLang.label;
        synth.speak(utterThis);
    }

    const Copy = () => {
        navigator.clipboard.writeText(translatedText);
    }

    const Save = () => {
        setIsSaved(!isSaved);
        // lưu bản dịch
    }

    useEffect(() => {
        if (inputText) {
            translateText(inputText);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [inputText, translatedText, ToLang.label]);

    return (
        <>
            <Flex className="trans__type" gap="large">
                <Button className={`trans__type--button ${selectedButton === "text" ? "selected" : ""}`} onClick={() => handleClick("text")} >
                    <Link to="/"><ZhihuOutlined /> Dịch văn bản</Link>
                </Button>
                <Button className={`trans__type--button ${selectedButton === "document" ? "selected" : ""}`} onClick={() => handleClick("document")} >
                    <Link to="/docs"><PaperClipOutlined /> Dịch tài liệu</Link>
                </Button>
            </Flex>

            <Flex justify="center">
                <Select
                    onChange={handleChangeFromLang}
                    options={languageOptions}
                    value={FromLang.label}
                    defaultValue={language['en-GB']}
                    className="select__lang"
                />
                <div className="swap select__lang"><SwapOutlined onClick={SwapLang} /></div>
                <Select
                    onChange={handleChangeToLang}
                    options={languageOptions}
                    value={ToLang.label}
                    defaultValue={language['vi-VN']}
                    className="select__lang"
                />
            </Flex>

            <Flex justify="space-around">
                <Row gutter={[12, 12]}>
                    <Col xl={12}>
                        <TextArea
                            value={inputText}
                            allowClear
                            rows={8}
                            cols={70}
                            className="margin-right"
                            onChange={(e) => setInputText(e.target.value)}
                        />
                        <div className="btn fromlang">
                            <Button shape="circle" onClick={SpeakInputText}>
                                <SoundOutlined />
                            </Button>
                            {token && translatedText !== "" ? (
                                <>
                                    <Button shape="circle" onClick={Save}>
                                        {isSaved ? <StarFilled /> : <StarOutlined />}
                                    </Button>
                                </>
                            ) : (<></>)}
                        </div>
                    </Col>
                    <Col xl={12}>
                        <TextArea
                            value={translatedText}
                            rows={8}
                            cols={70}
                            readOnly
                            className="text"
                        />
                        <div className="btn tolang">
                            <Button shape="circle" onClick={SpeakTranslatedText}>
                                <SoundOutlined />
                            </Button>
                            <Button shape="circle" onClick={Copy}>
                                <CopyOutlined />
                            </Button>
                        </div>
                    </Col>
                </Row>
            </Flex>
        </>
    )
}

export default Home;