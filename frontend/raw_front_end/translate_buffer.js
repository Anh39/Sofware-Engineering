function sleep(milisecond) {
    return new Promise(resolve => setTimeout(resolve, milisecond))
}

class TranslateManager {
    static jobs = [];
    static finished = false;
    static text_field = null;
    static running = false;
    static async translate(from_lang,to_lang,content,job) {
        let result = await fetch('/translate/text', {
            method: "POST",
            body: JSON.stringify({
                "from_language": from_lang,
                "to_language": to_lang,
                "content": content,
            })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                job['finished'] = true;
            }
        })
        .then(data => {
            let result = data["text"];
            return result;
        })
        job['finished'] = true;
        job['result'] = result;
    }
    static async add_queue(from_lang,to_lang,content) {
        let new_job = {
            'finished' : false,
            'result' : undefined
        }
        this.jobs.push(new_job);
        this.translate(from_lang,to_lang,content,new_job);
        if (this.running == false) {
            this.finished = false;
            this.running = true;
            this.process_translate();
        }
    }
    static async process_translate() {
        while (this.finished != true) {
            // console.log(this.jobs);
            for(let i=this.jobs.length-1;i>=0;i--) {
                let job = this.jobs[i];
                if (job['finished']) {
                    this.text_field.value = job['result'];
                    console.log(this.text_field);
                    if (i == this.jobs.length-1) {
                        this.finished = true;
                        console.log('Finished');
                    }
                    break;
                }
            }   
            await sleep(100);
        }
        this.clear();
    }
    static clear() {
        this.jobs = [];
        this.finished = false;
        this.running = false;
    }
}

export {TranslateManager}