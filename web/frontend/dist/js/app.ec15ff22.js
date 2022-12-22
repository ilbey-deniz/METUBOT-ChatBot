(function(){"use strict";var t={7860:function(t,e,a){var s=a(144),n=a(998),i=a(5716),r=a(4324),o=a(1625),l=a(3059),u=a(3687),c=a(7953),m=function(){var t=this,e=t._self._c;return e(n.Z,{style:{background:t.$vuetify.theme.themes[t.theme].background}},[e(i.Z,{attrs:{app:"",elevation:"4",height:t.appBarHeight}},[e("div",{staticClass:"d-flex align-center"},[e("router-link",{attrs:{to:"/"}},[e(o.Z,{staticClass:"mr-2",attrs:{alt:"METUBOT Logo",contain:"",src:a(7309),transition:"scale-transition",width:"166"}})],1)],1),"admin"===t.$route.name?e(c.qW,{staticClass:"text-h5"},[t._v("Yönetim")]):t._e(),e(u.Z),e("router-link",{staticClass:"mr-2 grey--text text-decoration-none",attrs:{to:"/yonetim"}},[t._v("Yönetim")]),e("router-link",{staticClass:"mr-2 grey--text text-decoration-none",attrs:{to:"/"}},[t._v("Metubot")]),t.$vuetify.theme.dark?e(r.Z,{on:{click:function(e){t.$vuetify.theme.dark=!1}}},[t._v(" mdi-weather-sunny ")]):e(r.Z,{on:{click:function(e){t.$vuetify.theme.dark=!0}}},[t._v(" mdi-weather-night ")])],1),e(l.Z,[e("router-view",{attrs:{"app-bar-height":t.appBarHeight}})],1)],1)},d=[],f={name:"App",watch:{$route:{immediate:!0,handler(t,e){document.title=t.meta.title||"METUBOT"}}},data:()=>({appBarHeight:64}),computed:{theme(){return this.$vuetify.theme.dark?"dark":"light"}}},p=f,h=a(3736),g=(0,h.Z)(p,m,d,!1,null,null,null),v=g.exports,y=a(8345),_=function(){var t=this,e=t._self._c;return e("metubot-chat",{style:t.fillScreen})},b=[],k=a(9582),x=a(4886),C=a(4127),w=a(266),Z=a(2118),S=a(9223),B=a(8224),M=a(5808),z=a(4525),T=a(5200),O=a(9608),F=a(9422),q=a(1713),$=a(7808),U=function(){var t=this,e=t._self._c;return e(Z.Z,{staticClass:"pa-0 fill-height"},[e(q.Z,{staticClass:"no-gutters elevation-4 fill-height"},[e(w.Z,{staticClass:"flex-grow-1 flex-shrink-0",attrs:{cols:"auto"}},[e(F.Z,{staticClass:"overflow-y-hidden fill-height"},[e(k.Z,{staticClass:"d-flex flex-column fill-height",attrs:{flat:""}},[e(x.ZB,{class:"flex-grow-1 overflow-y-auto "+t.scrollbarTheme},[t._l(t.messages,(function(a,s){return[e("div",{class:{"d-flex flex-row-reverse":a.isUser}},[e(O.Z,{attrs:{"offset-y":""},scopedSlots:t._u([{key:"activator",fn:function({on:s}){return[e(B.Z,{scopedSlots:t._u([{key:"default",fn:function({hover:n}){return[e(C.Z,t._g({staticClass:"pa-4 mb-2",staticStyle:{height:"auto","white-space":"pre"},attrs:{color:a.isUser?"primary":"red",dark:""}},s),[t._v(" "+t._s(a.content)+" "),e("sub",{staticClass:"ml-2",staticStyle:{"font-size":"0.5rem"}},[t._v(" "+t._s(a.created_at)+" ")]),n?e(r.Z,{attrs:{small:""}},[t._v("mdi-chevron-down")]):t._e()],1)]}}],null,!0)})]}}],null,!0)},[e(M.Z,[e(z.Z,[e(T.V9,[t._v("delete")])],1)],1)],1)],1)]})),e("transition",{attrs:{name:"fade"}},[t.waitingForAnswer?e(C.Z,{staticClass:"pa-4 mb-2 d-flex justify-center",staticStyle:{height:"auto","white-space":"normal",width:"70px"},attrs:{color:"red",dark:""}},[e("div",{staticClass:"dot-typing"})]):t._e()],1)],2),e(S.Z),e(x.ZB,{staticClass:"flex-shrink-1"},[e($.Z,{attrs:{label:"Mesaj",type:"text","no-details":"",outlined:"","hide-details":""},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.sendMessage.apply(null,arguments)}},scopedSlots:t._u([{key:"append-outer",fn:function(){return[e(r.Z,{on:{click:t.sendMessage,touchend:function(e){return e.preventDefault(),t.sendMessage.apply(null,arguments)}}},[t._v(" mdi-send ")])]},proxy:!0}]),model:{value:t.messageForm.content,callback:function(e){t.$set(t.messageForm,"content",e)},expression:"messageForm.content"}})],1)],1)],1)],1)],1)],1)},j=[],A=(a(7658),a(594)),Q=a(9367),H={name:"MetubotChat",props:{},data(){return{messages:[],messageForm:{content:"",isUser:!0,created_at:"11:11am"},waitingForAnswer:!0,socketIoSocket:null}},mounted(){this.socketIoSocket=(0,Q.io)(),this.socketIoSocket.on("chat answer",(t=>{this.waitingForAnswer=!1,""===t&&(t="Sualinize maalesef mütenasip bir yanıt bulamamaktayım. Başka sorunuz varsa lütfen sakınmayınız."),this.messages.push({content:t,isUser:!1,created_at:this.getClock()})}))},methods:{sendMessageToServer(){A.Z.post("/",{question:this.chatMessage})},getClock(){let t=new Date,e=t.getHours(),a=t.getMinutes();return`${e}:${a}`},sendMessage(){""===this.messageForm.content||this.waitingForAnswer||(this.messageForm.created_at=this.getClock(),this.messages.push(this.messageForm),this.socketIoSocket.emit("chat question",this.messageForm.content),this.messageForm={content:"",isUser:!0,created_at:null},this.waitingForAnswer=!0)}},computed:{scrollbarTheme(){return this.$vuetify.theme.dark?"dark-scrollbar":"light-scrollbar"}}},E=H,P=(0,h.Z)(E,U,j,!1,null,"05218754",null),I=P.exports,L={name:"Home",props:{appBarHeight:Number},components:{MetubotChat:I},data(){return{fillScreen:{position:"fixed",top:this.appBarHeight+"px",left:"50%",transform:"translate(-50%)",width:"100%",height:`calc(100% - ${this.appBarHeight}px)`,overflow:"auto"}}}},V=L,D=(0,h.Z)(V,_,b,!1,null,"4c13c650",null),Y=D.exports,R=function(){var t=this,e=t._self._c,a=t._self._setupProxy;return e("div",{staticClass:"app"},[e(a.Sidebar),e("router-view")],1)},N=[],W=a(7423),G=function(){var t=this,e=t._self._c,a=t._self._setupProxy;return e(W.Z,{attrs:{color:"bg2"}},[e("aside",{class:""+(a.is_expanded?"is-expanded":"")},[e("div",{staticClass:"logo"},[e("img",{attrs:{src:a.logoURL,alt:"Vue"}})]),e("div",{staticClass:"menu-toggle-wrap"},[e("button",{staticClass:"menu-toggle",on:{click:a.ToggleMenu}},[e("span",{staticClass:"material-icons"},[t._v("keyboard_double_arrow_right")])])]),e("h3",[t._v("Menu")]),e("div",{staticClass:"menu"},[e("router-link",{staticClass:"button",attrs:{to:"/"}},[e("span",{staticClass:"material-icons"},[t._v("home")]),e("span",{staticClass:"text"},[t._v("Home")])]),e("router-link",{staticClass:"button",attrs:{to:"/yonetim/dashboards"}},[e("span",{staticClass:"material-icons"},[t._v("dashboard")]),e("span",{staticClass:"text"},[t._v("Dashboard")])]),e("router-link",{staticClass:"button",attrs:{to:"/yonetim/tables"}},[e("span",{staticClass:"material-icons"},[t._v("table_chart")]),e("span",{staticClass:"text"},[t._v("Tables")])]),e("router-link",{staticClass:"button",attrs:{to:"/yonetim/charts"}},[e("span",{staticClass:"material-icons"},[t._v("pie_chart")]),e("span",{staticClass:"text"},[t._v("Charts")])])],1),e("div",{staticClass:"flex"}),e("div",{staticClass:"menu"},[e("router-link",{staticClass:"button",attrs:{to:"/settings"}},[e("span",{staticClass:"material-icons"},[t._v("settings")]),e("span",{staticClass:"text"},[t._v("Settings")])])],1)])])},J=[],K=a.p+"img/metubot-logo-nameless.4fe9eedf.png",X={__name:"Sidebar",setup(t){const e=(0,s.ref)("true"===localStorage.getItem("is_expanded")),a=()=>{e.value=!e.value,localStorage.setItem("is_expanded",e.value)};return{__sfc:!0,is_expanded:e,ToggleMenu:a,logoURL:K}}},tt=X,et=(0,h.Z)(tt,G,J,!1,null,"54eab6b0",null),at=et.exports,st={__name:"AdminView",setup(t){return{__sfc:!0,Sidebar:at}}},nt=st,it=(0,h.Z)(nt,R,N,!1,null,null,null),rt=it.exports,ot=a(5163),lt=function(){var t=this,e=t._self._c;return e(k.Z,{staticClass:"card"},[e(x.EB,[t._v(" Sorulan Sorular "),e(u.Z),e($.Z,{attrs:{"append-icon":"mdi-magnify",label:"Arama"},model:{value:t.search,callback:function(e){t.search=e},expression:"search"}})],1),e(ot.Z,{attrs:{headers:t.headers,items:t.questions,search:t.search,"items-per-page":5,"items-per-page-text":"hl","no-results-text":"Sonuç bulunamadı.","no-data-text":"Soru bulunmamaktadır.","footer-props":{"items-per-page-text":"Sayfa başı gösterilecek soru sayısı:"}},scopedSlots:t._u([{key:"footer.page-text",fn:function(e){return[t._v(" "+t._s(e.pageStart)+" - "+t._s(e.pageStop)+" / "+t._s(e.itemsLength)+" ")]}}],null,!0)})],1)},ut=[],ct={name:"MetubotAskedQuestions",components:{AdminView:rt},data(){return{search:"",questions:[{question:"Bugün ne yiyeceğiz?",matchedQuestion:"Bugün pilav üstü odtü kavurma yiyeceğiz.",similarity:.8},{question:"Şifremi nasıl öğrenebilirim?",matchedQuestion:"Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",similarity:.6},{question:"Bugün ne yiyeceğiz?",matchedQuestion:"Bugün pilav üstü odtü kavurma yiyeceğiz.",similarity:.8},{question:"Şifremi nasıl öğrenebilirim?",matchedQuestion:"Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",similarity:.6},{question:"Bugün ne yiyeceğiz?",matchedQuestion:"Bugün pilav üstü odtü kavurma yiyeceğiz.",similarity:.8},{question:"Şifremi nasıl öğrenebilirim?",matchedQuestion:"Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",similarity:.6},{question:"Bugün ne yiyeceğiz?",matchedQuestion:"Bugün pilav üstü odtü kavurma yiyeceğiz.",similarity:.8},{question:"Şifremi nasıl öğrenebilirim?",matchedQuestion:"Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",similarity:.6}],headers:[{text:"Sorulan Soru",align:"start",sortable:!0,value:"question"},{text:"Eşleşen Soru",value:"matchedQuestion"},{text:"Benzerlik",value:"similarity"}]}}},mt=ct,dt=(0,h.Z)(mt,lt,ut,!1,null,"fbc6dec4",null),ft=dt.exports;s["default"].use(y.ZP);const pt=[{path:"/",name:"metubot",component:Y,meta:{title:"METUBOT"}},{path:"/yonetim",name:"admin",children:[{path:"tables",component:ft}],component:rt,meta:{title:"METUBOT Yönetim"}}],ht=new y.ZP({routes:pt});var gt=ht,vt=a(707),yt=a.n(vt);a(8556);s["default"].config.productionTip=!1,s["default"].use(yt()),new s["default"]({router:gt,vuetify:new(yt())({theme:{dark:!1,themes:{light:{background:"#f5f0f1",bg2:"#64748b"},dark:{bg2:"#2c2a2a"}}}}),render:t=>t(v)}).$mount("#app")},7309:function(t,e,a){t.exports=a.p+"img/metubot-logo.828f8f1b.png"}},e={};function a(s){var n=e[s];if(void 0!==n)return n.exports;var i=e[s]={exports:{}};return t[s].call(i.exports,i,i.exports,a),i.exports}a.m=t,function(){var t=[];a.O=function(e,s,n,i){if(!s){var r=1/0;for(c=0;c<t.length;c++){s=t[c][0],n=t[c][1],i=t[c][2];for(var o=!0,l=0;l<s.length;l++)(!1&i||r>=i)&&Object.keys(a.O).every((function(t){return a.O[t](s[l])}))?s.splice(l--,1):(o=!1,i<r&&(r=i));if(o){t.splice(c--,1);var u=n();void 0!==u&&(e=u)}}return e}i=i||0;for(var c=t.length;c>0&&t[c-1][2]>i;c--)t[c]=t[c-1];t[c]=[s,n,i]}}(),function(){a.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return a.d(e,{a:e}),e}}(),function(){a.d=function(t,e){for(var s in e)a.o(e,s)&&!a.o(t,s)&&Object.defineProperty(t,s,{enumerable:!0,get:e[s]})}}(),function(){a.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"===typeof window)return window}}()}(),function(){a.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)}}(),function(){a.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})}}(),function(){a.p="/"}(),function(){var t={143:0};a.O.j=function(e){return 0===t[e]};var e=function(e,s){var n,i,r=s[0],o=s[1],l=s[2],u=0;if(r.some((function(e){return 0!==t[e]}))){for(n in o)a.o(o,n)&&(a.m[n]=o[n]);if(l)var c=l(a)}for(e&&e(s);u<r.length;u++)i=r[u],a.o(t,i)&&t[i]&&t[i][0](),t[i]=0;return a.O(c)},s=self["webpackChunkmetubot"]=self["webpackChunkmetubot"]||[];s.forEach(e.bind(null,0)),s.push=e.bind(null,s.push.bind(s))}();var s=a.O(void 0,[998],(function(){return a(7860)}));s=a.O(s)})();
//# sourceMappingURL=app.ec15ff22.js.map