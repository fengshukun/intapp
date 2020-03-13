Vue.prototype.is_url=function(URL){
    var Expression=/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/;
    var objExp=new RegExp(Expression);
    if(objExp.test(URL)==true){
        return true;
    }else{
        return false;
    }
}

Vue.prototype.$axios = axios;
var axios_instance = axios.create({
    // baseURL:'http://127.0.0.1:39001/',
    timeout:180000,
    // params:{signparam:''},
    withCredentials: false,// `withCredentials` 表示跨域请求时是否需要使用凭证
    // transformRequest: [function (data) {
    //     data = Qs.stringify(data);
    //     return data;
    // }],
    
})
//请求拦截
axios_instance.interceptors.request.use(axiosconfig=>{
    // var login=localStorage.getItem('login');
    // if(login){
    //     login=Base64.decode(login);
    //     login=JSON.parse(login);
    //     var login_random=Math.ceil(Math.random()*100);
    //     var login_time=config.time;
    //     var login_sign=md5(login.password+login_time+login_random);
    //     config.signparam=Base64.encode(JSON.stringify({'login_random':login_random,'login_id':login.login_id,'login_sign':login_sign,'login_time':login_time}));
    //     axiosconfig.params.signparam=config.signparam;
    // }
    // axiosconfig.baseURL=config.defaultURL;
    return axiosconfig;
},error=>{
    return Promise.reject(error);
})
//响应拦截
axios_instance.interceptors.response.use(res=>{
    return res;
},error=>{
    return Promise.reject(error);
})
//get请求
Vue.prototype.get=function(url,params={},text=null){
    self=this
    if(text){//self.$message({message: text,type: 'error'});
        var Loading = self.$loading({lock: true,text: text,spinner: 'el-icon-loading',background: 'rgba(0, 0, 0, 0.7)'});
    }
    return new Promise((resolve,reject) => {
        axios_instance.get(url,{params:params})
        .then(res => {
            if(text){setTimeout(function(){Loading.close();},100)}
            if(res.data.code==0){
                resolve(res.data);
            }else{
                self.$message({message: res.data.msg,type: 'error'});
            }
        })
        .catch(err => {
            if(text){setTimeout(function(){Loading.close();},100)}
            if (err.response) {
                if (err.response.data.hasOwnProperty('msg')){
                    msg=err.response.data.msg
                }else{
                    msg=err.response.data
                }
                self.$message({message: "错误码："+err.response.status+","+msg,type: 'error'});
            }else if (err.request){
                self.$message({message: "无法链接到服务器",type: 'error'});
            }else{
                self.$message({message: "网络异常，",type: 'error'});
            }
            reject(err)
        })
    })
}
//delete请求
Vue.prototype.delete=function(url,params={},text=null){
    self=this
    if(text){//self.$message({message: text,type: 'error'});
        var Loading = self.$loading({lock: true,text: text,spinner: 'el-icon-loading',background: 'rgba(0, 0, 0, 0.7)'});
    }
    return new Promise((resolve,reject) => {
        axios_instance.delete(url,{data:params})
        .then(res => {
            if(text){setTimeout(function(){Loading.close();},100)}
            if(res.data.code==0){
                resolve(res.data);
            }else{
                self.$message({message: res.data.msg,type: 'error'});
            }
        })
        .catch(err => {
            if(text){setTimeout(function(){Loading.close();},100)}
            if (err.response) {
                if (err.response.data.hasOwnProperty('msg')){
                    msg=err.response.data.msg
                }else{
                    msg=err.response.data
                }
                self.$message({message: "错误码："+err.response.status+","+msg,type: 'error'});
            }else if (err.request){
                self.$message({message: "无法链接到服务器",type: 'error'});
            }else{
                self.$message({message: "网络异常，",type: 'error'});
            }
            reject(err)
        })
    })
}
//post请求
Vue.prototype.post=function(url,params={},text=null){
    self=this
    if(text){
        var Loading = self.$loading({lock: true,text: text,spinner: 'el-icon-loading',background: 'rgba(0, 0, 0, 0.7)'});
    }
    return new Promise((resolve,reject) => {
        axios_instance.post(url,params)
        .then(res => {
            if(text){setTimeout(function(){Loading.close();},100)}
            if(res.data.code==0){
                resolve(res.data);
            }else{
                self.$message({message: res.data.msg,type: 'error'});
            }
        })
        .catch(err => {
            if(text){setTimeout(function(){Loading.close();},100)}
            if (err.response) {
                if (err.response.data.hasOwnProperty('msg')){
                    msg=err.response.data.msg
                }else{
                    msg=err.response.data
                }
                self.$message({message: "错误码："+err.response.status+","+msg,type: 'error'});
            }else if (err.request){
                self.$message({message: "无法链接到服务器",type: 'error'});
            }else{
                self.$message({message: "网络异常，",type: 'error'});
            }
            reject(err)
        })
    })
}
//put请求
Vue.prototype.put=function(url,params={},text=null){
    self=this
    if(text){
        var Loading = self.$loading({lock: true,text: text,spinner: 'el-icon-loading',background: 'rgba(0, 0, 0, 0.7)'});
    }
    return new Promise((resolve,reject) => {
        axios_instance.put(url,params)
        .then(res => {
            if(text){setTimeout(function(){Loading.close();},100)}
            if(res.data.code==0){
                resolve(res.data);
            }else{
                self.$message({message: res.data.msg,type: 'error'});
            }
        })
        .catch(err => {
            if(text){setTimeout(function(){Loading.close();},100)}
            if (err.response) {
                if (err.response.data.hasOwnProperty('msg')){
                    msg=err.response.data.msg
                }else{
                    msg=err.response.data
                }
                self.$message({message: "错误码："+err.response.status+","+msg,type: 'error'});
            }else if (err.request){
                self.$message({message: "无法链接到服务器",type: 'error'});
            }else{
                self.$message({message: "网络异常，",type: 'error'});
            }
            reject(err)
        })
    })
}

//get请求 获取内容
Vue.prototype.getcontent=function(url,text=null,data={}){
    self=this
    var params={};
    if(data){
        params=data;
    }
    if(text){
        var Loading = self.$loading({lock: true,text: text,spinner: 'el-icon-loading',background: 'rgba(0, 0, 0, 0.7)'});
    }
    return new Promise((resolve,reject) => {
        axios_instance.get(url,{params:params})
        .then(res => {
            if(text){setTimeout(function(){Loading.close();},100)}
            resolve(res.data);
        })
        .catch(err => {
            if(text){setTimeout(function(){Loading.close();},100)}
            reject(err)
        })
    })
}
//复制内容到剪贴板
Vue.prototype.copy=function(content){
    if(content){
        let val = content; // 要复制的内容
        document.addEventListener('copy', save); // 监听浏览器copy事件
        document.execCommand('copy'); // 执行copy事件，这时监听函数会执行save函数。
        document.removeEventListener('copy', save); // 移除copy事件
        function save(e) {
            e.clipboardData.setData('text/plain', val); // 剪贴板内容设置
            e.preventDefault();
        }
        self.$message({message: "复制成功：",type: 'success'});
    }else{
        self.$message({message: "内容不能为空：",type: 'error'});
    }
}

Vue.prototype.time_date=function(time,datestatus=false){
    var date = new Date(time*1000);
    if (datestatus){
        return date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate()+"  "+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds();
    }else{
        var dqtime=Date.parse(new Date())/1000;
        var k='';
        var sjc=dqtime-time;
        if(sjc<=30){
            k="刚刚";
        }else if(sjc<=60){
            k=sjc+"秒前";
        }else if(sjc<=60*60){
            k=Math.floor(sjc/60)+"分钟前";
        }else if(sjc<=60*60*24){
            k=Math.floor(sjc/(60*60))+"小时前";
        }else if(sjc<=60*60*24*7){
            k=Math.floor(sjc/(60*60*24))+"天前";
        }else if(sjc<=60*60*24*30){
            k=Math.floor(sjc/(60*60*24*7))+"星期前";
        }else if(sjc<=60*60*24*30*12){
            k=(date.getMonth()+1)+"月"+date.getDate()+"日";
        }else{
            k=date.getFullYear()+"年"+(date.getMonth()+1)+"月";
        }
        return k;
    }
}

Vue.prototype.time_date1=function(time){
    var date = new Date(time*1000);
    var dqtime=Date.parse(new Date())/1000;
    var k='';
    var sjc=dqtime-time;
    if(sjc<=60*60*24){
        k=date.getHours()+":"+date.getMinutes()+":"+date.getSeconds();
    }else if(sjc<=60*60*24*7){
        k=Math.floor(sjc/(60*60*24))+"天前";
    }else if(sjc<=60*60*24*30){
        k=Math.floor(sjc/(60*60*24*7))+"星期前";
    }else if(sjc<=60*60*24*30*12){
        k=(date.getMonth()+1)+"月"+date.getDate()+"日";
    }else{
        k=date.getFullYear()+"年"+(date.getMonth()+1)+"月";
    }
    return k;
}