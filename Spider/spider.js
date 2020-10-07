/*
spider.js
Copyright@takamitsu hamada
License      :  BSD License
Documentation : http://vsrx.site/valkyriedocs/html/index.html#spider-code-library
*/
const ms = "http://vsrx.site";
let ver = "20190328",
$w = window,
$d = $w.document,
$gtag="getElementsByTagName",
$gid="getElementById",
$qS = "querySelector",
$qSA = "querySelectorAll",
$l="length",
$aEL="addEventListener",
$rEL="removeEventListener",
$atE="attachEvent",
$deE="detachEvent",
$crE="createElement",
$cTN="createTextNode",
$aC="appendChild",
$sA="setAttribute",
$na = navigator,
$nan = $na.appName,
$nav = $na.appVersion,
$np = $na.platform,
$ua = $na.userAgent,
$ualc = $na.toLowerCase,
$npl = $na.plugins,
$nmt = $na.mimeTypes,
$sn = screen,
$int = parseInt,
$si = setInterval,
$ci = clearInterval,
$sti = setTimeout,
$cti = clearTimeout,
$host,$dbname,$user,$password,$table,
$db = "&host=" + $host + "&dbname=" + $dbname + "&user=" + $user + "&password=" + $password + "&table=" + $table;
const $script = $d[$gtag]("script");
for(let i=0;i<$script[$l];i++)src = $script[i].getAttribute("src") || $script[i].src;
let spd = "Spider";
let $raf = $w.requestAnimationFrame ||
                  $w.mozRequestAnimationFrame ||
                  $w.webkitRequestAnimationFrame ||
                  $w.msRequestAnimationFrame;
let $caf = $w.cancelAnimationFrame ||
                  $w.mozcancelAnimationFrame ||
                  $w.webkitcancelAnimationFrame ||
                  $w.mscancelAnimationFrame;

let now = $w.performance &&
(performance.now ||
performance.mozNow ||
performance.msNow ||
performance.oNow ||
performance.webkitNow);

const gettime = () => {
  return (now && now.call(performance)) || (new Date().getTime());
}
//load method
const load = (func) => {
    //$w.onload = func;
    $sti(func,$script[$l]*100);
    //var s = spider("");
    //s.domloaded(func);
}
const spider = (() => {
    const $stfl = ($ua.indexOf("firefox") || $ua.indexOf("opera") || $ua.indexOf("webkit")) ? "cssFloat" : "styleFloat";
    const $lp = ("https:" == $d.location.protocol) ? "https://ssl" : "http://www";
//spider class build
    const constructor = function(id){
        if(!(this instanceof spider))return new spider(id);
        this.id =  (id.match(/^(div)/g)) ? $d[$gtag]("div")[$int(id.slice(3,id.length))] :
        (id.match(/^(p[1-100])/g)) ? $d[$gtag]("p")[$int(id.slice(1,id.length))] :
        (id.match(/^(a[1-100])/g)) ? $d[$gtag]("a")[$int(id.slice(1,id.length))] :
        (id.match(/^(ul)/i)) ? $d[$gtag]("ul")[$int(id.slice(2,id.length))] :
        (id.match(/^(li)/i)) ? $d[$gtag]("li")[$int(id.slice(2,id.length))] :
        (id.match(/^(input)/i)) ? $d[$gtag]("input")[$int(id.slice(5,id.length))] :
        (id.match(/^(button)/i)) ? $d[$gtag]("button")[$int(id.slice(6,id.length))] :
        (id.match(/^(span)/i)) ? $d[$gtag]("span")[$int(id.slice(4,id.length))] :
        (id.match(/^(script)/g)) ? $d[$gtag]("script")[$int(id.slice(6,id.length))] :
        (id.match(/^(head)/g)) ? $d[$gtag]("head")[$int(id.slice(4,id.length))] :
        (id.match(/^(iframe)/g)) ? $d[$gtag]("iframe")[$int(id.slice(6,id.length))] :
        (id.match(/^(title)/g)) ? $d[$gtag]("title")[$int(id.slice(5,id.length))] :
        (id.match(/^(section)/g)) ? $d[$gtag]("section")[$int(id.slice(7,id.length))] :
        (id.match(/^(nav)/g)) ? $d[$gtag]("nav")[$int(id.slice(3,id.length))] :
        (id.match(/^(article)/g)) ? $d[$gtag]("article")[$int(id.slice(7,id.length))] :
        (id.match(/^(aside)/g)) ? $d[$gtag]("aside")[$int(id.slice(5,id.length))] :
        (id.match(/^(hgroup)/g)) ? $d[$gtag]("hgroup")[$int(id.slice(5,id.length))] :
        (id.match(/^(footer)/g)) ? $d[$gtag]("footer")[$int(id.slice(6,id.length))] :
        (id.match(/^(address)/g)) ? $d[$gtag]("address")[$int(id.slice(7,id.length))] :
        (id.match(/^(figure)/g)) ? $d[$gtag]("figure")[$int(id.slice(6,id.length))] :
        (id.match(/^(figcaption)/g)) ? $d[$gtag]("figcaption")[$int(id.slice(10,id.length))] :
        (id.match(/^(time)/g)) ? $d[$gtag]("time")[$int(id.slice(4,id.length))] :
        (id.match(/^(video)/g)) ? $d[$gtag]("video")[$int(id.slice(5,id.length))] :
        (id.match(/^(audio)/g)) ? $d[$gtag]("audio")[$int(id.slice(5,id.length))] :
        (id.match(/^(source)/g)) ? $d[$gtag]("source")[$int(id.slice(6,id.length))] :
        (id.match(/^(canvas)/g)) ? $d[$gtag]("canvas")[$int(id.slice(6,id.length))] :
        (id.match(/^(area)/g)) ? $d[$gtag]("area")[$int(id.slice(4,id.length))] :
        (id.match(/^(img)/g)) ? $d[$gtag]("img")[$int(id.slice(3,id.length))] :
        (id == "body") ? $d.body :
        (id == "document") ? $d :
        (id == "window") ? $w :
        $d[$gid](id);
        this.version = ver;
        this.ver=$nav;
        this.agent=$ua;
        this.dom=$d[$gid] ? 1 : 0;
        this.mac=this.agent.indexOf("Mac")>-1;
        this.fx=this.agent.indexOf("firefox") > -1;
        this.webkit = $ua.indexOf('AppleWebKit') > -1;
        this.gecko = $ua.indexOf('Gecko') > -1 && $ua.indexOf('KHTML') == -1;
        this.mobileSafari = !!$ua.match(/Apple.*Mobile.*Safari/);
        this.google_chrome = $ua.match(/Chrome\/([\.\d]+)/);
        this.safari = $ua.match(/Safari\/([\.\d]+)/);
        return this;
    }
//spider Method
    constructor.prototype = {
//require method
    require : function(src){
        const $head = $d[$gtag]("head")[0];
        (src.match(/\.(js)/i) || src.match(/\.(txt)/i)) ?
        (aec=this.addElement('script',$head),aec.type = "text/javascript",aec.src = src) :
        (src.match(/\.(css)/i)) ?
        (aec=this.addElement("link",$head),aec.rel = "stylesheet",aec.href = src,aec.type = "text/css") :
        (src.match(/\.(cgi)/i) || src.match(/\.(php)/i) || src.match(/\.(rb)/i) || src.match(/\.(pl)/i) || src.match(/\.(py)/i)) ?
        this.httpRequest(src,"GET",() => {}) : 0;
        return this;
    },
//addElement method
    addElement : function(newelement,baseelement){
        aec = $d[$crE](newelement);
        baseelement[$aC](aec);
        return aec;
    },
//addListener method
    addListener : function(eventType,func,cap){
        let eT = eventType;
        let ti = this.id;
        ($w[$aEL]) ? ti[$aEL](eT,func,cap) :
           ($w[$atE]) ? ti[$atE]("on" + eT,() => {func.call(ti,$w.event);}) :
            ti["on" + eT] = func;
        return this;
    },
//removeListener method
    removeListener : function(eventType,func,cap){
        let eT = eventType;
        let ti = this.id;
        ($w[$rEL]) ? ti[$rEL](eT,func,cap) :
            ($w[$deE]) ? ti[$deE]("on" + eT,() => {func.call(ti,$w.event);}) :
        ti["on" + eT] = func;
        return this;
    },
//click method
    click : function(func){
        this.addListener("click",func,"once");
        return this;
    },
//mouseover method
    mouseover : function(func){
        this.addListener("mouseover",func,false);
        return this;
    },
//mouseout method
    mouseout : function(func){
        this.addListener("mouseout",func,false);
        return this;
    },
//mousemove method
    mousemove : function(func){
        this.addListener("mousemove",func,false);
        return this;
    },
//mouseup method
    mouseup : function(func){
        this.addListener("mouseup",func,false);
        return this;
    },
//mousedown method
    mousedown : function(func){
        this.addListener("mousedown",func,false);
        return this;
    },
//keyDown method
    keyDown : function(func){
        spider("document").addListener("keydown",func,"once");
        return this;
    },
//scroll method
    scroll : function(func){
      this.addListener("scroll",func,"once");
      return this;
    },
//scrollanim method
    scrollanim : function(anim_mode){
      let animationFlag = false;
      let saobj = this.id;
      let spiderobj = this;
       spider("window").scroll(() => {
           let scrolltop = document.body.scrollTop || document.documentElement.scrollTop;
           let windowheight = $w.innerHeight;
           let offset = saobj.offsetTop;
           if(scrolltop > offset-windowheight+300){
              if(!animationFlag){
                  if(anim_mode == "fadein"){
                      spiderobj.css("fadein",{speed:10});
                  }else if(anim_mode == "spreadl"){
                      spiderobj.css("spreadx",{speed:1,end:1325}).css("fadein",{speed:1});
                  }else if(anim_mode == "spreadr"){
                      spiderobj.css("spreadx",{speed:-1,end:0}).css("fadein",{speed:1});
                  }else if(anim_mode == "spreadu"){
                      spiderobj.css("spready",{speed:1,end:400}).css("fadein",{speed:1});
                  }
                  animationFlag = true;
              }
            }
          });
        return this;
    },
//scrollto method
   scrollto : function(target){
     let bcr = $d.getElementById(target).getBoundingClientRect();
     let positionX = bcr.left + window.pageXOffset;
     let positionY = bcr.top + window.pageYOffset;
     $w.scrollTo(positionX,positionY);
     return this;
   },
//html method
    html : function(mode,option){
        if(mode == "import"){
            let cobj = $d[$crE]("object");
            this.id.appendChild(cobj);
            with(cobj){
                type = "text/html";
                data = option.data;
                classid = "clsid:25336920-03F9-11CF-8FD0-00AA00686F13";
                id = option.cid;
                innerHTML = option.data;
            }
            with(cobj.style){
                width=option.width+"px";
                height=option.height+"px";
                margin="0px";
                padding="0px";
            }
            return cobj;
        }
        if(mode == "ajax"){
            let rtb = this.id;
            return this.httpRequest(option.url,{method:"GET",
                 func : function(xml){rtb.innerHTML = xml.responseText;}});
        }
        if(mode == "inner"){
            this.id.innerHTML = option.string;
        }
        if(mode == "add"){
            this.id.innerHTML += option.string;
        }
        if(mode == "pjax"){
            this.html("ajax",{str:option.url});
            if($w.history && $w.history.pushState){
                history.pushState(state,"",option.url);
            }
            let th = this;
            let state = $w[$aEL]("popstate",(e) => {
            if (!e.state) return;
            this.html(location.pathname,"ajax");
            },false);
        }
        if(mode == "iframe"){
            this.id.innerHTML = "<iframe src='"+option.src+"' style='width:640px;height:580px'></iframe>";
        }
        return this;
    },
//tool method
   tool : function(mode ,option){
        if(mode == "imgload"){
            let ip = [];
            for(let i=0;i<option.array[$l];i++){
                ip[i] = new Image();
                ip[i].src = option.array[i];
            }
            return ip;
        }
        if(mode == "title"){
            ($d.title == option.string) ? this.require(option.src) : 0;
        }
        if(mode == "href"){
            this.id.href = option.url;
        }
        if(mode == "scriptVersion"){
            const $script = $d[$gid]("script");
            for(let i=0;i<$script[$l];i++){
                if($script[i].type == "text/javascript")$script[i].type = "text/javascript" + ";version = " + option.version;
            }
        }
        if(mode == "appendMenuItem"){
            let msli1 = $d[$crE]("li");
            let msa1 = $d[$crE]("a");
            let mst1 = $d[$cTN](option.menuitem);
            msa1.href=option.url;
            msa1[$aC](mst1);
            msli1[$aC](msa1);
            this.id.appendChild(msli1);
        }
        if(mode == "createCookie"){
            let cookie = option.name + "=" +escape(option.value) + ";";
            (option.expires instanceof Date) ?
                (isNaN(option.expires.getTime()) ? (option.expires = new Date()) : 0) :
            (option.expires = new Date(new Date().getTime() + $int(option.expires)*1000*60*60*24));
            cookie += "expires=" + option.expires.toGMTString() + ";";
            option.path ? (cookie += "path=" + option.path + ";") : 0;
            option.domain ? (cookie += "domain=" + option.domain + ";") : 0;
            $d.cookie = cookie;
        }
        if(mode == "getCookie"){
            let regexp = new RegExp("(?:^" + option.name + "|;\\s*" + option.name + ")=(.*?)(?:;|$)","g");
            let result = regexp.exec($d.cookie);
            return (result === null) ? null : result[1];
        }
        if(mode == "deleteCookie"){
            if(this.cookie("delete",{name:option.name}))this.cookie("create",{name:option.name,value:"",expires:-1});
        }
        if(mode == "domloaded"){
            $d.addEventListener("DOMContentLoaded",func,false);
        }
        if(mode == "xpath"){
            return option.xmlDoc.evaluate(path,xmlDoc.documentElement,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        }
        if(mode == "historyback"){
            return history.back();
        }
        if(mode == "historyforward"){
            return history.forword();
        }
        if(mode == "historygo"){
            return history.go(num);
        }
        if(mode == "historylength"){
            return history.length;
        }
        if(mode == "referrer"){
            return $d.referrer;
        }
        if(mode == "linkarray"){
            for(let i=0;i<$d.links[$l];i++){
                [$d.links[$l]][i] = $d.links[i].href;
           }
        }
        if(mode == "reload"){
            $sti(() => {location.reload();},option.time);
        }
        if(mode == "scrollMessage"){
            let str = option.string;
            count = 0;
            let fo = $d.createElement("form");
            let ip = $d.createElement("input");
            ip.type = "text";
            ip.size = "40";
            let ips = ip.style;
            with(ips){
                backgroundColor = "#000000";
                color = "#ffffff";
                fontSize = "100pt";
                border = "0";
            }
            ip.id = "scrollMsg";
            fo.appendChild(ip);
            this.id.appendChild(fo);
            sM = () =>{
                $cti(tID);
                $w.status = str;
                $d.getElementById("scrollMsg").value = str;
                str = str.substring(1,str.length) + str.substring(0,1);
                tID = $sti(() => {sM();},120);
            }
            tID = $sti(() => {sM();},120);
        }
        if(mode == "typing"){
            let fo = $d.createElement("form");
            let ip = $d.createElement("input");
            ip.type = "text";
            ip.size = "40";
            let ips = ip.style;
            with(ips){
                backgroundColor = "#000000";
                color = "#ffffff";
                fontSize = "100pt";
                border = "0";
            }
            ip.id = "typingMsg";
            fo.appendChild(ip);
            this.id.appendChild(fo);
            start = () => {
                str = "";
                i = 0;
                tiid = $sti(() => {message();},150);
            }
            message = () => {
                $cti(tiid);
                    (i<option.string.length) ?
                (str = str + option.string.charAt(i),i++,$d[$gid]("typingMsg").value = str,tiid = $sti(() => {message();},150)) :
                start();
            }
            return start();
        }
        if(mode == "imageanimation"){
            let i = 1;
            let sobj = this;
            $si(() => {
                sobj.html("inner",{string:"<img src='" + option.array[i] + "'/>"});
                i++;
                (i>option.array[$l]) ? i=0 : 0;
            },option.speed);
        }
        if(mode == "stopwatch"){
            let [h,m,s,active] = [0,0,0,0];
            let fo = $d.createElement("form");
            let ip1 = $d.createElement("input");
            with(ip1){
                type="text";
                size = "42";
                id = "stimer";
            }
            let ip2 = $d.createElement("input");
            with(ip2){
                type = "button";
                value = "start";
                onclick = () => {
                    if(active == 0){
                        active = 1;
                        tiid = $si(() => {
                            s++;
                            (s == 60) ? (m++,s =0,(m == 60) ? (h++,m = 0) : 0) : 0;
                            date.setHours(h);
                            date.setMinutes(m);
                            date.setSeconds(s);
                            $d.getElementById("stimer").value = date.toLocaleString();
                        },1000);
                    }
                }
            }
            let ip3 = $d.createElement("input");
            with(ip3){
                type = "button";
                value = "stop";
                onclick = stop;
            }
            with(fo){
                appendChild(ip1);
                appendChild(ip2);
                appendChild(ip3);
            }
            this.id.appendChild(fo);
            let date = new Date();
            var stop = () => {
                (active == 1) ? (active = 0,$ci(tiid)) : 0;
            }
            return (() =>{
                let [h,m,s,active] = [0,0,0,0];
                stop();
                date.setHours(h);
                date.setMinutes(m);
                date.setSeconds(s);
                $d.getElementById("stimer").value = date.toLocaleString();
            })();
       }
       if(mode == "accordion"){
            let newstyle = $d.createElement("style");
            newstyle.type = "text/css";
            $d.getElementsByTagName("head")[0].appendChild(newstyle);
            css = document.styleSheets[0];
            let idx = $d.styleSheets[0].cssRules.length;
            with(css){
                insertRule(".ac-container{max-width: 400px;border: 1px solid #ccc;border-top: none;}",idx);
                insertRule(".ac-container label {height: 30px;line-height: 1.8;font-size: 20px;padding: 5px 20px;display: block;cursor: pointer;color: #666;background: #eee;border-top: 1px solid #ccc;}",idx);
                insertRule(".ac-container input {display: none;}",idx);
                insertRule(".ac-container article {overflow: hidden;height: 0;transition: 0.6s;}",idx);
                insertRule(".ac-container input:checked ~ article {height: 150px;border-top: 1px solid #ccc;}",idx);
           }
       }
       if(mode == "animationbutton"){
           let newstyle = $d.createElement("style");
           newstyle.type = "text/css";
           $d.getElementsByTagName("head")[0].appendChild(newstyle);
           css = $d.styleSheets[0];
           let idx = $d.styleSheets[0].cssRules.length;
           with(css){
               insertRule(".circlePositioner {margin-left: auto;margin-right: auto;width: 400px;text-align: center;margin-top: 150px;background-color: #0881AA;}",idx);
               insertRule(".mainCircle {background-color: #0881AA;width: 200px;height: 200px;border-radius: 50%;display: inline-block;overflow: hidden;cursor: pointer;opacity: .99;transition: all 1s ease-in-out;}",idx);
               insertRule(".spinningContainer {background-color: #efefef;height: 50px;width: 100%;margin-top: 75px;position: relative;animation: mymoveR 1s ease-in-out;transform: scaleY(2);transition: all 2s cubic-bezier(.18, 1.51, .85, 1.4);}",idx);
               insertRule(".mainCircle:hover .overlay {background-color: #7C9FAB;transition: all .3s ease-in-out;}",idx);
               insertRule(".mainCircle:hover .overlay p {color: white;transition: all .3s ease-in-out;}",idx);
               insertRule(".mainCircle:hover .spinningContainer {-webkit-filter: blur(5px);animation: mymove 1s cubic-bezier(1, .22, 1, .92), myscale 2s 1s ease-in-out;}",idx);
               insertRule("@keyframes mymove {from {transform: rotate(0deg);}to{transform: rotate(1080deg);}}",idx);
               insertRule("@keyframes mymoveR {from {transform: rotate(1080deg);}to {transform: rotate(0deg);}}",idx);
               insertRule("@keyframes myscale {0% {transform: scaleY(2);}25% {transform: scaleY(2.5);}50% {transform: scaleY(3);}75% {transform: scaleY(3.5);}100% {transform: scaleY(4);}}",idx);
               insertRule(".mainCircle:hover {background-color: white;transition: all 1s ease-in-out;transition-delay: .8s;}",idx);
               insertRule(".leftContainer {background-color: rgba(255, 255, 255, 0.79);height: 50px;width: 50px;float: left;}",idx);
               insertRule(".rightContainer {background-color: rgba(255, 255, 255, 0.79);height: 50px;width: 50px;float: right;}",idx);
               insertRule(".overlay {background-color: #46626B;height: 190px;width: 190px;position: relative;margin-left: auto;margin-right: auto;margin-top: -120px;border-radius: 50%;transition: all .3s ease-in-out;}",idx);
               insertRule(".overlay p {position: relative;text-align: center;margin-left: auto;margin-right: auto;margin-top: 39%;display: inline-block;font-family: 'Sigmar One', cursive;font-size: 16pt;transition: all .3s ease-in-out;}",idx);
           }
       }
       return this;
   },
//command method
   command : function(cmd,htmlsrc){
       var ti = this;
       cheet(cmd,() => {
           ti.html("iframe",{src:htmlsrc});
       });
       return this;
   },
//css method
    css : function(mode,option){
        var ti = this.id.style;
        if(mode == "addClass"){
            this.id.className += option.css_class || this.id.classList.add(option.css_class);
        }
        if(mode == "removeClass"){
            this.id.className = "" || this.id.classList.remove(option.css_class);
        }
        if(mode == "addRule"){
            var ss = $d.styleSheets[option.cssnum];
            if($d.all){
                ss.addRule(option.selector,option.style,option.index);
            }else{
                ss.insertRule(option.rule,option.index);
            }
        }
        if(mode == "removeRule"){
            var ss = $d.styleSheets[option.cssnum];
            if($d.all){
                ss.removeRule(option.index);
            }else{
                ss.deleteRule(option.index);
            }
        }
        if(mode == "setCSS"){
            ti.cssText = option.css;
        }
        if(mode == "targetBlank"){
            var $a = $d[$gtag]("a");
            for(var i=0;i<$a.length;i++){
                (!($a[i].href == "#")) ? $a[i].target = "_blank" : 0;
            }
        }
        if(mode == "position"){
            (option.position == "absolute") ? ti.position = "absolute" :
                (option.position == "relative") ? ti.position = "relative" : 0;
            ti.left = option.x + "px";
            ti.top = option.y + "px";
        }
        if(mode == "size"){
            ti.width = option.width + "px";
            ti.height = option.height + "px";
        }
        if(mode == "zindex"){
            ti.zIndex = option.z;
        }
        if(mode == "float"){
            (this.ie) ?
                (ti.styleFloat = option.type) : (ti.cssFloat = option.type);
        }
        if(mode == "margin"){
            ti.margin = option.value;
        }
        if(mode == "padding"){
            ti.padding = option.value;
        }
        if(mode == "background"){
            with(ti){
                backgroundImage = 'url('+ option.src + ')';
                backgroundRepeat = option.repeat;
                backgroundColor = option.color;
                backgroundPosition = option.position;
            }
        }
        if(mode == "font"){
            with(ti){
                fontSize = option.size+'px';
                color = option.fontcolor;
                fontFamily = option.fontfamily;
                textDexoration = option.decoration;
            }
        }
        if(mode == "clip"){
            (option.left < 0) ? option.left = 0 : 0;
            (option.right > option.lx) ? option.right = option.lx : 0;
            (option.left > option.right) ? option.left = option.right : 0;
            (option.up < 0) ? option.up = 0 : 0;
            (option.left > option.ly) ? option.left = option.ly : 0;
            (option.up > option.left) ? option.up = option.left : 0;
            ti.clip = "rect(" + " " + option.right + " " + option.down + " " + option.left +")";
        }
        if(mode == "visible"){
            ti.visibility = "visible";
            ti.display = "block";
        }
        if(mode == "hidden"){
            ti.visibitily = "hidden";
            ti.display = "none";
        }
        if(mode == "cssiframe"){
            ti.overflow = "scroll";
        }
        if(mode == "opacity"){
            with(ti){
                opacity = option.opacity/100;
                mozOpacity = option.opacity/100;
                filter = 'alpha(opacity = ' + option.opacity + ')';
            }
        }
        if(mode == "innerwidth"){return $d.body.clientWidth;}
        if(mode == "innerheight"){return $d.body.clientHeight;}
        if(mode == "rotate"){
            with(ti){
                webkitTransform = "rotate("+option.deg+"deg)";
                MozTransform = "rotate("+option.deg+"deg)";
                transform = "rotate("+option.deg+"deg)";
            }
        }
        if(mode == "skewx"){
            ti.webkitTransform = "skewX("+option.deg+"deg)";
            ti.MozTransform = "skewX("+option.deg+"deg)";
            ti.transform = "skewX("+option.deg+"deg)";
        }
        if(mode == "skewy"){
            var ti = this.id.style;
            with(ti){
                webkitTransform = "skewY("+option.deg+"deg)";
                MozTransform = "skewY("+option.deg+"deg)";
                transform = "skewY("+option.deg+"deg)";
            }
        }
        if(mode == "transtlate"){
            with(ti){
                webkitTransform = "translate("+option.x+","+option.y+")";
                MozTransform = "translate("+option.x+","+option.y+")";
                transform = "translate("+option.x+","+option.y+")";
            }
        }
        if(mode == "scale"){
           with(ti){
               webkitTransform = "scale("+option.scale+")";
               MozTransform = "scale("+option.scale+")";
               transform = "scale("+option.scale+")";
           }
        }
        if(mode == "boxShadow"){
            with(ti){
                webkitBoxShadow = "black 2px 2px 5px";
                MozBoxShadow = "black 2px 2px 5px";
                boxShadow = "black 2px 2px 5px";
            }
        }
        if(mode == "transform"){
            ti.webkitTransform = "translate("+option.x+"px,"+option.y+"px) rotate("+option.deg+"deg)";
            ti.webkitTransformOrigin = "left top";
        }
        if(mode == "transition"){
            ti.webkitTransitionProperty = "all";
            ti.webkitTransitionDelay = option.delay+"s";
            ti.webkitTransitionDuration = option.duration+"s";
            ti.webkitTransitionTimingFunction = "ease-in-out";
        }
        if(mode == "borderRadius"){
            ti.webkitBorderRadius = option.radius+"px";
        }
        if(mode == "gradient"){
            ti.background = "-webkit-gradient(linear,left top,left bottom,from(#990),color-stop(0.5,#f0f),to(#066))";
        }
        if(mode == "animation"){
            ti.webkitAnimationName = "test";
            ti.webkitAnimationDuration = "400ms";
            ti.webkitAnimationIterationCount = 10;
            ti.webkitAnimationTimingFunction = "ease-in-out";
        }
        var [fps,ds] = [0,ti];
        const now = $w.performance.now();
        if(mode == "spreadx"){
            ds.width = "0";
            (function step(){
                const aid = $raf(step);
                ds.width = $int(ds.width) + fps + "px";
                fps += option.speed;
                ($int(ds.width) > option.end) ? $caf(aid) : 0;
            })();
        }
        if(mode == "spready"){
            ds.height = "0";
            (function step(){
                const aid = $raf(step);
                ds.height = $int(ds.height) + fps + "px";
                fps += option.speed;
                ($int(ds.height) > option.end) ? $caf(aid) : 0;
            })();
        }
        if(mode == "spreadxy"){
            ds.width = "0";
            ds.height = "0";
            (function step(){
                 const aid = $raf(step);
                 ds.width = $int(ds.width) + fps + "px";
                 ds.height = $int(ds.height) + fps + "px";
                 fps += option.speed;
                ($int(ds.height) > option.end) ? $caf(aid) : 0;
            })();
        }
        if(mode == "shrinkx"){
            (function step(){
                const aid = $raf(step);
                ds.width = $int(ds.width) + fps + "px";
                fps -= option.speed;
                ($int(ds.width) < option.end) ? $caf(aid) : 0;
            })();
        }
        if(mode == "shrinky"){
           (step = () =>{
                const aid = $raf(step);
                ds.height = $int(ds.height) + fps + "px";
                fps -= option.speed;
                ($int(ds.height) < option.end) ? $caf(aid) : 0;
            })();
        }
        if(mode == "shrinkxy"){
            (function step(){
                const aid = $raf(step);
                ds.width = $int(ds.width) + fps + "px";
                ds.height = $int(ds.height) + fps + "px";
                fps -= option.speed;
                ($int(ds.width) < option.end) ? $caf(aid) : 0;
            })();
        }
        if(mode == "movex"){
          let fps = 0;
          (function step(){
            const aid = $raf(step);
            ds.left = $int(ds.left) + fps + "px";
            fps += option.speed;
            (fps > 0) ?
                  ($int(ds.left) > option.end) ? $caf(aid) : 0 :
                  ($int(ds.left) < option.end) ? $caf(aid) : 0;
          })();
        }
        if(mode == "movey"){
          let fps = 0;
          (function step(){
              const aid = $raf(step);
              ds.top = $int(ds.top) + fps + "px";
              fps += option.speed;
              (fps > 0) ?
                    ($int(ds.top) > option.end) ? $caf(aid) : 0 :
                    ($int(ds.top) < option.end) ? $caf(aid) : 0;
          })();
        }
        if(mode == "movexy"){
          let fps =0;
          (function step(){
                const aid = $raf(step);
                ds.left = $int(ds.left) + fps + "px";
                ds.top = $int(ds.top) + fps + "px";
                fps +=option.speed;
                (fps > 0) ?
                    ($int(ds.left) > option.end) ? $caf(aid) : 0 :
                ($int(ds.left) < option.end) ? $caf(aid) : 0;
            })();
        }
        if(mode == "fadein"){
            let dobj = this;
            let opc = 0;
            (function step(){
                const aid = $raf(step);
                dobj.css("opacity",{opacity:opc});
                opc += option.speed;
                (opc > 100) ? $caf(aid) : 0;
            })();
        }
        if(mode == "fadeout"){
            let dobj = this;
            let opc = 100;
            (function step(){
                const aid = $raf(step);
                dobj.css("opacity",{opacity:opc});
                opc -= option.speed;
                (opc < 0) ? $caf(aid) : 0 ;
            })();
        }
        if(mode == "rotateeffect"){
            let i = 0;
            let reff = this;
            $si(() => {
                reff.css("rotate",{deg:i});
                i+=option.speed;
            },50);
        }
        if(mode == "scaleeffect"){
            let i = 1;
            let seff = this;
            let ssi =  $si(() => {
                seff.css("scale",{scale:i});
                i+=0.1;
            },50);
            (i > option.scale) ? $ci(ssi) : 0;
        }
        if(mode == "location"){
            let i = 0;
            $si(() => {
               $d.title = option.array[i++ % option.array[$l]];
            },100);
        }
        if(mode == "csssprites"){
            let fg = $d[$gid](option.id).style;
            with(fg){
                width = option.width + "px";
                height = option.height + "px";
                backgroundImage = "url(" + option.imgsrc + ")";
                backgroundRepeat = "no-repeat";
            }
            let ix = 0;
            $si(() => {
                fg.style.backgroundPosition = "0 -" + ix + "px";
                ix += hi;
                if(ix>hi*option.xx)ix=0;
            },option.speed);
        }
        if(mode == "hiddeniframeconst"){
            let a = $d[$gtag]("a");
            let urlA = [];
            for(let i=0;i<a[$l];i++)urlA.push(a[i].href);
            let divb = $d[$cE]("div");
            $d.body[$aC](divb);
            divb.id = id;
            for(let j=0;j<urlA[$l];j++){
                if(!(urlA[j].match(/#/i) || urlA[j].match(mat))){
                    ifl = $d[$cE]("iframe");
                    divb[$aC](ifl);
                    with(ifl){
                        id = "iframe_id" + j;
                        src = urlA[j];
                        nodeValue = "URL";
                    }
                    let ifs = ifl.style;
                    with(ifs){
                        width = "0px";
                        height = "0px";
                        visibility = "hidden";
                       display = "none";
                    }
                }
            }
        }
        if(mode == "hiddeniframerandom"){
            let a = $d[$gtag]("a");
            let urlA = [];
            for(let i=0;i<a.length;i++)urlA.push(a[i].href);
            let divc = $d.createElement("div");
            $d.body.appendChild(divc);
            divc.id = id;
            let urlB = [];
            for(let i=0;i<urlA[$l];i++){
                if(!(urlA[i].match(/#/i) || urlA[i].match(mat))){
                    urlB.push(urlA[i]);
                }
            }
            let n = Math.floor(Math.random()*urlB.length);
            ifl = $d[$cE]("iframe");
            divc.appendChild(ifl);
            with(ifl){
                id = "iframe_id"+id;
                src = urlB[n];
                nodeValue = "URL";
            }
            let ifs = ifl.style;
            with(ifs){
                width = "0px";
                height = "0px";
                visibility = "hidden";
                display = "none";
            }
        }
        if(mode == "hiddeniframeremove"){
            while($d[$gid](id).hasChildNodes()){
                $d[$gid](id).removeChild($d[$gid](id).firstChild);
            }
        }
        if(mode == "colorchange"){
            let i = 0;
            $si(() => {
                $d.body.style.backgroundColor = option.array[i];
                i++;
                (i > option.array[$l]-1) ? i = 0 : 0;
            },1000);
        }
        return this;
    },
//info method
    info : function(mode){
        if(mode == "date"){
            const date = new Date();
            this.id.innerHTML += "Today\'s Date \-\>"
                + date.getFullYear()+ "\."
                + (date.getMonth()+1) + "\."
                + date.getDate() + "<br />"
                + "Time \-\>" + date.getHours() + "\:"
                + date.getMinutes() + "\:"
                + date.getSeconds() + "<br />";
        }
        if(mode == "browser"){
            const br = "<br/>";
            this.id.innerHTML += 'Browser :' + $nan
                + br +'Version :' + $na.appVersion
                + br +'CodeName :' + $na.appCodeName
                + br + 'Language :' + $na.browserLanguage
                + br + 'Platform :' + $np
                + br + 'UserAgent :' + $na.userAgent
                + br + 'JAVA Enabled :' + $na.javaEnabled()
                + br + 'Cookie Enabled :' + $na.cookieEnabled + br;
        }
        if(mode == "screen"){
            const br = "<br/>";
            this.id.innerHTML += "Screen Width :" + $sn.width
                + br + "Screen Height :" + $sn.height
                + br + "Avail Width :" + $sn.availWidth
                + br + "Avail Height :" + $sn.availHeight
                + br + "Color Depth :" + $sn.colorDepth
                + br + "Font Smoothing :" + $sn.fontSmoothingEnabled + br;
        }
        return this;
    },
//createLayer method
    createLayer : function(layid,option){
        let aC = this.addElement("div",$d.body);
        aC.id = layid;
        let obj = $d[$gid](layid);
        const px = "px";
        with(obj.style){
            position = "absolute";
            width = option.width + px;
            height = option.height + px;
            left = option.x + px;
            top = option.y + px;
            zIndex = option.z;
            margin = 0;
            padding = 0;
            color = option.fontC;
            backgroundColor = option.bgC;
            innerHTML = option.html;
        }
        return obj;
    },
//XMLObject method
    XMLObject : function(){
        return (typeof XMLHttpRequest != "undefined") ? new XMLHttpRequest() : (new ActiveXObject("Msxml2.XMLHTTP") || new ActiveXObject("Microsoft.XMLHTTP"));
    },
//httpRequest method
    httpRequest : function(url,option){
        var hObj = this.XMLObject();
        (!hObj) ? eval("alert('Error : Not Found XML');return false;") : 0;
        let hR = () => {
            return (hObj.status == 200) ? option.func(hObj) : 0;
        }
        hObj.addEventListener("loadend",hR);
        if(option.method == "GET"){
            hObj.open(option.method,url.match(/\?/g) ? url : url + "?" + (new Date).getTime(),!0);
            hObj.send("");
        }
        if(option.method == "POST"){
            hObj.open(option.method,url.match(/\?/g) ? url : url + "?" + (new Date).getTime(),!0);
            hObj.setRequestHeader("Content-Type","application/x-www-urlencoded,charset=UTF-8");
            hObj.send(option.query);
        }
        return this;
    },
//loadXML method
    loadXML : function(url){
        let hObj = this.XMLObject();
        (!hObj) ? eval("alert('Error : Not Found XML');return false;") : 0;
        hObj.open("GET",url.match(/\?/g) ? url : url + "?" + (new Date).getTime(),!1);
        (url.match(/\.(xml)/i)) ? hObj.overrideMimeType("text/xml") : 0;
        hObj.send("");
        return hObj.responseXML;
        return this;
    },
//xmlTransform method
    xmlTransform : function(xml_src,xslt_src){
        let $xml,xslt,xslProc;
        if(!$d.all){
            $xml = $d.implementation.createDocument("","",null);
            xslt = $d.implementation.createDocument("","",null);
        }else{
            $xml = new ActiveXObject("Msxml2.DOMDocument");
            xslt = new ActiveXObject("Msxml2.FreeThreadedDOMDocument");
        }
        $xml.async = !1;
        xslt.async = !1;
        $xml.load(xml_src);
        xslt.load(xslt_src);
        if(!$d.all){
            xslProc = new XSLTProcessor();
            xslProc.importStylesheet(xslt);
            let newDoc = xslProc.transformToFragment($xml,document);
            this.id.innerHTML = "";
            let aC = this.addElement("div",$d.body);
            aC.id = newDoc;
        }else{
            let xslTemp = new ActiveXObject("Msxml2.XSLTemplate");
            xslTemp.stylesheet = xslt;
            xslProc = xslTemp.createProcessor();
            xslProc.input = $xml;
            this.id.innerHTML = $xml.transformNode(xslt);
        }
        return this;
    },
//slideShow method
    slideShow : function(array){
        for(let i=0;i<array[$l]-1;i++){
            let gas = $d[$gid](array[i]).style;
            gas.width = "100%";
            //gas.style.styleFloat = "left";
            gas.visibility = "hidden";
        }
        let i = 0;
        spider(array[i]).css("visible");
        spider(array[i]).keyDown((e) => {
            var ek = e.keyCode-38;
            var al = array[$l]-1;
            i += ek;
            (i>=0) ?
                (i>al) ? i=0 : spider(array[i-1]).css("hidden") :
            (i<al) ? i=al : spider(array[i+1]).css("hidden");
            spider(array[i]).css("visible");
        });
        spider(array[i]).mousedown(() => {
            spider(array[i]).css("hidden");
            spider(array[i+1]).css("visibile");
            if(i<array[$l]-1){i++;}
        });
    },
//imgChange method
    imgChange : function(option){
    let i = 0;
    this.css("size",{width:option.width,height:option.height});
    this.html('add',{str:'<img src="' + option.dir + '/' + option.array[i] + '" id = "io"/>'});
    keyDown((e) => {
        var ek = e.keyCode - 38;
        var io = $d[$gid]("io");
        var da = option.dir + "/" + option.array[i];
        var al = array.length;
        i += ek;
        (ek > 0) ?
        (i > al) ? i = 0 : io.src =  da :
        (i < 0) ? i = $int(al) : io.src = da;
    });
    return this;
    },
//moviePlayer method
    moviePlayer : function(src_array,postersrc,options){
    var vi = $d.createElement("video");
    with(vi){
            autoplay = "true";
            autobuffer = "true";
            poster = postersrc;
            controls = options.control_set;
            muted = options.mute_set;
            loop = options.loop_set;
            preload = options.preload_set;
            style.width = options.width+"px";
            style.height = options.height+"px";
    }
    for(var i=0;i<src_array.length;i++){
        var vc = $d.createElement("source");
        vc.src = src_array[i];
        if(vc.src.match(/(.mp4)/i)){
        vc.type = "video/mp4";
        }
        if(vc.src.match(/(.ogg)/i)){
        vc.type = "video/ogg";
        }
        if(vc.src.match(/(.webm)/i)){
        vc.type = "video/webm";
        }
        vi.appendChild(vc);
    }
    this.id.appendChild(vi);
    return this;
    },
//audioPlayer method
    audioPlayer : function(audio_array){
    let au = $d.createElement("audio");
    au.id = "auid";
    let ausrc = $d.createElement("source");
    for (let i=0;i<audio_array[$l];i++){
        ausrc.src = audio_array[i];
        if(ausrc.src.match(/mp3/i)){
        ausrc.type = "audio/mp3";
        }
        if(ausrc.src.match(/ogg/i)){
        ausrc.type = "audio/ogg";
        }
        au.appendChild(ausrc);
    }
    let audiv = $d.createElement("div");
    let b1 = $d.createElement("button");
    b1.onclick = () => {
        $d[$gid]("auid").play();
    }
    b1.innerHTML = "Play";
    let b2 = $d.createElement("button");
    b2.onclick = () => {
        $d[$gid]("auid").pause();
    }
    b2.innerHTML = "Pause";
    let b3 = $d.createElement("button");
    b3.onclick = () => {
        $d[$gid]("auid").volume += 0.1;
    }
    b3.innerHTML = "Increase Volume";
    let b4 = $d.createElement("button");
    b4.onclick = () => {
        $d[$gid]("auid").volume -= 0.1;
    }
    b4.innerHTML = "Decrease Volume";
    with(audiv){
        appendChild(b1);
        appendChild(b2);
        appendChild(b3);
        appendChild(b4);
    }
    let apid = this.id;
    apid.appendChild(au);
    apid.appendChild(audiv);
    return this;
    },
//parseXML method
    parseXML : function(url,method){
    this.id.html(url,method,(xml) => {
        xt = xml.responseText;
        ($w.ActiveXObject) ?
        (xmlDoc = new ActiveXObject("Microsoft.XMLDOM"),xmlDoc.async = "false",xmlDoc.loadXML(xt)) :
        ($w.XMLHttpRequest) ?
        (parser = new DOMParser(),xmlDoc = parser.parseFromString(xt,"text/xml"),dec = xmlDoc.getElementsByTagBame("title"),$d.getElementById("xc3").innerHTML = dec[1].childNodes[0].nodeValue) : 0;
    });
    return this;
    },
//selectImage method
    selectImage : function(dir,array,titleA){
    var dih = this.id;
    dih.innerHTML = '<img src="' + dir + "/"
        + array[0]
        + '" id="sun"/>'
        + '<form><p><select id = "channel" size="1" onchange="sC(this)">';
    for(var i=0;i<array[$l];i++){
        $d[$gid]("channel").innerHTML += '<option value="' + i + '">' + titleA[i] + '</option>';
    }
    dih.innerHTML += '</form>';
    sC = (parts) => {
        for(var j=0;j<array[$l];j++){
        fname = parts.options[parts.selectedIndex].value;
        (fname==j) ? ($d[$gid]("sun").src = dir + array[j]) : 0;
        }
    }
    return this;
    },
//meltdown method
    meltdown : function(){
        let db = $d.body;
        let all = db[$gtag]("*");
        let bH = Math.max(db.scrollHeight,Math.max(db.clientHeight, $d.documentElement.clientHeight));
        db.innerHTML = '<div style="width:100%;overflow:hidden;height:'+bH+'px;">' + db.innerHTML + '</div>';
        let tE = [];
        for(let i=0;i<all.length;i++){
            if(!all[i].offsetParent)continue;
            all[i].point = ((ele) => {
                for(x=y=0;ele;){
                    x += ele.offsetLeft;
                    y += ele.offsetTop;
                    ele = ele.offsetParent;
                }
                return {x:x,y:y}
            })(all[i]);
            tE[tE.length] = all[i];
        }
        for(let j=0;j<tE.length-1;j++){
            ele = tE[j];
            eP = ele.parentNode;
            (eP.point) ? (ele._x = ele.point.x - eP.point.x,ele._y = ele.point.y - eP.point.y,ele.parentX = eP.point.x,ele.parentY = eP.point.y):(ele._x = ele.point.x,ele._y = ele.point.y);
            with(ele.style){
                position = 'absolute';
                width = (ele.clientWidth == 0) ? ele.offsetWidth : Math.min(ele.offsetWidth,ele.clientWidth) + 'px';
                height = (ele.clientHeight == 0) ? ele.offsetHeight : Math.min(ele.offsetHeight,ele.clientHeight) + 'px';
                left = ele._x + 'px';
                top = ele._y + 'px';
                margin = '0px';
                padding = '0px';
            }
            new (function(tar){
                this.ele = tar;
                this.speed = 1;
                this.left = tar.offsetLeft;
                this.lRS = Math.random()*3;
                this.start = (dl) => {
                    this.tarY = bH - this.ele.point.y;
                    var scp = this;
                    $sti(() => {scp.loop()},dl);
                }
                this.loop = () => {
                    if(this.tarY<this.ele.offsetTop)return;
                    var _top = this.ele.offsetTop;
                this.ele.style.top = this.ele.offsetTop + $int(this.speed) + 'px';
                    this.speed *= 2;
                    this.left += this.lRS;
                    this.ele.style.left = $int(this.left) + 'px';
                    if(this.ele.offsetTop==_top)return;
                    var scp = this;
                    $sti(() => {scp.loop()},70);
                }
            })(tar=tE[tE.length-1-j]).start(j*30);
        }
        return this;
    },
//matrixEffect method
    matrixEffect : function(){
        let bt_root = this.id;
        bt_root.style.visibility = "hidden";
        let bt_nodes = [];
        let bt_text = [];
        let bt_tumble = [];
        let bt_maxsize = bt_count = 0;
        let bt_spin = () => {
            let $sss=new spider("");
            if($sss.dom && !($sss.mac && $sss.ie)) bt_godeep(bt_root);
            bt_root.style.visibility = "visible";
            if($sss.dom && !($sss.mac && $sss.ie)) bt_sponge();
        }
        let bt_chartype = Math.floor(Math.random()*2);
        let digit = () => {
            if(bt_chartype == 0)
                return Math.floor(Math.random()*2);
            else if(bt_chartype == 1)
                return '_';
            else
                return '_';
        }
        let bt_haschars = (s) => {
            return s.replace(/"\r|\n"/g,'').length;
        }
        let bt_godeep = (o) => {
            for(let i=0;i<o.childNodes.length;i++){
                if(o.childNodes[i].childNodes){
                    bt_godeep(o.childNodes[i]);
                }
                if(o.childNodes[i].nodeName == '#text' && bt_haschars(o.childNodes[i].nodeValue)){
                    let p = bt_nodes.length;
                    bt_nodes[p] = o.childNodes[i];
                    bt_text[p] = o.childNodes[i].nodeValue;
                    bt_tumble[p] = [];
                    for(let u=0;u<o.childNodes[i].nodeValue.length;u++){
                        bt_tumble[p][u] = u;
                    }
                    if(o.childNodes[i].nodeValue.length > bt_maxsize){
                        bt_maxsize = o.childNodes[i].nodeValue.length;
                    }
                    bt_tumble[p].sort((w1,w2) => {return Math.floor(Math.random()*3)-1;});
                    o.childNodes[i].nodeValue = "";
                }
            }
        }
        let bt_sponge = () => {
            for(let i = 0;i<bt_nodes.length;i++){
                if(bt_count < bt_tumble[i].length){
                    bt_nodes[i].nodeValue += (bt_text[i].charAt(bt_count) == " ") ? " " : digit(1);
                }
            }
            bt_count++;
            if(bt_count < bt_maxsize){
                $sti(bt_sponge,20);
            }else{
                bt_count = 0;
                $sti(bt_unsponge,350);
            }
        }
        let bt_repchar = (str,ch,pos) => {
            let out = "";
            for(let i=0;i<str.length;i++){
                if(i == pos) out += ch;
                else out += str.charAt(i);
            }
            return out;
        }
        let bt_unsponge = () => {
            for(let i=0;i<bt_nodes.length;i++){
                if(bt_count <= bt_tumble[i].length){
                    bt_nodes[i].nodeValue = bt_repchar(bt_nodes[i].nodeValue, bt_text[i].charAt(bt_tumble[i][bt_count]), bt_tumble[i][bt_count]);
                }
            }
            bt_count++;
            if(bt_count < 10) $sti(bt_unsponge,30);
            else if(bt_count < bt_maxsize) $sti(bt_unsponge,5);
            else (() => {
                bt_nodes = null;
                bt_text = null;
                bt_tumble = null;
            })();
        }
        $sti(() => {
            let $sss = spider("");
            if($sss.dom && !($sss.mac && $sss.ie)) bt_godeep(bt_root);
            bt_root.style.visibility = "visible";
            if($sss.dom && !($sss.mac && $sss.ie)) bt_sponge();
        },100);
    },
//particle method
    particle : function(r,g,b){
    let canvas = this.id;
    let ctx = canvas.getContext("2d");
    let pcs = [];
    let _num = 20;
    for(let i=0;i<_num;i++){
        pcs[i] = new (function(){
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.xvel = Math.random() * 5 - 2.5;
        this.yvel = Math.random() * 5 - 2.5;
        this.update = () => {
            this.x += this.xvel;
            this.y += this.yvel;
            this.yvel += 0.1;
            (this.x > canvas.width || this.x < 0) ? this.xvel = -this.xvel : 0;
            (this.y > canvas.height || this.y < 0) ? this.yvel = -this.yvel : 0;
        }
        })();
    }
    ctx.lineWidth = "10";
    ctx.strokeStyle = "rgb(" + r + "," + g + "," + b + ")";
    let loop = () => {
        ctx.clearRect(0,0,canvas.width,canvas.height);
        for(let i=0;i<_num;i++){
                pcs[i].update();
                with(ctx){
                    beginPath();
                    moveTo(pcs[i].x,pcs[i].y);
                    lineTo(pcs[i].x - pcs[i].xvel,pcs[i].y - pcs[i].yvel);
                    stroke();
                    closePath();
                }
        }
        $sti(loop,10);
    }
    loop();
    return this;
    }
}
    return constructor;
})();

//cheet.js
"use strict";!function(){function keydown(e){var id,k=e?e.keyCode:event.keyCode;if(!held[k]){held[k]=!0;for(id in sequences)sequences[id].keydown(k)}}function keyup(e){var k=e?e.keyCode:event.keyCode;held[k]=!1}function reset(){var k;for(k in held)held[k]=!1}function on(obj,type,fn){obj.addEventListener?obj.addEventListener(type,fn,!1):obj.attachEvent&&(obj["e"+type+fn]=fn,obj[type+fn]=function(){obj["e"+type+fn](window.event)},obj.attachEvent("on"+type,obj[type+fn]))}var cheet,Sequence,sequences={},keys={backspace:8,tab:9,enter:13,"return":13,shift:16,"⇧":16,control:17,ctrl:17,"⌃":17,alt:18,option:18,"⌥":18,pause:19,capslock:20,esc:27,space:32,pageup:33,pagedown:34,end:35,home:36,left:37,L:37,"←":37,up:38,U:38,"↑":38,right:39,R:39,"→":39,down:40,D:40,"↓":40,insert:45,"delete":46,0:48,1:49,2:50,3:51,4:52,5:53,6:54,7:55,8:56,9:57,a:65,b:66,c:67,d:68,e:69,f:70,g:71,h:72,i:73,j:74,k:75,l:76,m:77,n:78,o:79,p:80,q:81,r:82,s:83,t:84,u:85,v:86,w:87,x:88,y:89,z:90,"⌘":91,command:91,kp_0:96,kp_1:97,kp_2:98,kp_3:99,kp_4:100,kp_5:101,kp_6:102,kp_7:103,kp_8:104,kp_9:105,kp_multiply:106,kp_plus:107,kp_minus:109,kp_decimal:110,kp_divide:111,f1:112,f2:113,f3:114,f4:115,f5:116,f6:117,f7:118,f8:119,f9:120,f10:121,f11:122,f12:123,equal:187,"=":187,comma:188,",":188,minus:189,"-":189,period:190,".":190},NOOP=function(){},held={};Sequence=function(str,next,fail,done){var i;for(this.str=str,this.next=next?next:NOOP,this.fail=fail?fail:NOOP,this.done=done?done:NOOP,this.seq=str.split(" "),this.keys=[],i=0;i<this.seq.length;++i)this.keys.push(keys[this.seq[i]]);this.idx=0},Sequence.prototype.keydown=function(keyCode){var i=this.idx;return keyCode!==this.keys[i]?(i>0&&(this.idx=0,this.fail(this.str),cheet.__fail(this.str)),void 0):(this.next(this.str,this.seq[i],i,this.seq),cheet.__next(this.str,this.seq[i],i,this.seq),++this.idx===this.keys.length&&(this.done(this.str),cheet.__done(this.str),this.idx=0),void 0)},cheet=function(str,handlers){var next,fail,done;"function"==typeof handlers?done=handlers:null!=handlers&&(next=handlers.next,fail=handlers.fail,done=handlers.done),sequences[str]=new Sequence(str,next,fail,done)},cheet.disable=function(str){delete sequences[str]},on(window,"keydown",keydown),on(window,"keyup",keyup),on(window,"blur",reset),on(window,"focus",reset),cheet.__next=NOOP,cheet.next=function(fn){cheet.__next=null===fn?NOOP:fn},cheet.__fail=NOOP,cheet.fail=function(fn){cheet.__fail=null===fn?NOOP:fn},cheet.__done=NOOP,cheet.done=function(fn){cheet.__done=null===fn?NOOP:fn},window.cheet=cheet,"undefined"!=typeof module&&(module.exports=cheet)}();

//import 3rd library

spider("").require("https://cdnjs.cloudflare.com/ajax/libs/three.js/102/three.min.js");
