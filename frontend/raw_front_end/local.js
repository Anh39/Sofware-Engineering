class UserInfo {
    static logged;
    static name;
    static uuid;
    static save() {
        localStorage.clear();
        localStorage.setItem('user_logged',this.logged);
        localStorage.setItem('user_name',this.name);
        localStorage.setItem('user_uuid',this.uuid);
    }
    static load() {
        this.logged = localStorage.getItem('user_logged') || false;
        this.name = localStorage.getItem('user_name') || undefined;
        this.uuid = localStorage.getItem('user_uuid') || undefined;
        if (this.logged == 'true') {
            this.logged = true;
        }
    }
    static get_dict() {
        let result = {
            "logged" : this.logged,
            "name" : this.name,
            "uuid" : this.uuid,
        }
        return result;
    }
    static save_dict(input_dict) {
        this.logged = input_dict["logged"];
        this.name = input_dict["name"];
        this.uuid = input_dict["uuid"];
        this.save();
    }
    static load_and_get_dict() {
        this.load();
        return this.get_dict();
    }
    static clear(){
        localStorage.clear();
        this.load();
    }
}

export{UserInfo}