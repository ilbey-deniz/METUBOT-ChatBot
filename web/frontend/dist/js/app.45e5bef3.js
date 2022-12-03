(function(){"use strict";var e={7592:function(e,t,n){var i=n(144),a=n(998),s=n(5716),r=n(4324),o=n(1625),l=n(3059),u=n(3687),c=n(7953),m=function(){var e=this,t=e._self._c;return t(a.Z,[t(s.Z,{attrs:{app:"",elevation:"4",height:e.appBarHeight}},[t("div",{staticClass:"d-flex align-center"},[t("router-link",{attrs:{to:"/"}},[t(o.Z,{staticClass:"mr-2",attrs:{alt:"METUBOT Logo",contain:"",src:n(7309),transition:"scale-transition",width:"166"}})],1)],1),"admin"===e.$route.name?t(c.qW,{staticClass:"text-h5"},[e._v("Yönetim")]):e._e(),t(u.Z),t("router-link",{staticClass:"mr-2 grey--text text-decoration-none",attrs:{to:"/yonetim"}},[e._v("Yönetim")]),t("router-link",{staticClass:"mr-2 grey--text text-decoration-none",attrs:{to:"/"}},[e._v("Metubot")]),e.$vuetify.theme.dark?t(r.Z,{on:{click:function(t){e.$vuetify.theme.dark=!1}}},[e._v(" mdi-weather-sunny ")]):t(r.Z,{on:{click:function(t){e.$vuetify.theme.dark=!0}}},[e._v(" mdi-weather-night ")])],1),t(l.Z,[t("router-view",{attrs:{"app-bar-height":e.appBarHeight}})],1)],1)},f=[],d={name:"App",watch:{$route:{immediate:!0,handler(e,t){document.title=e.meta.title||"METUBOT"}}},data:()=>({appBarHeight:64})},h=d,p=n(1001),g=(0,p.Z)(h,m,f,!1,null,null,null),y=g.exports,v=n(8345),k=function(){var e=this,t=e._self._c;return t("metubot-chat",{attrs:{"app-bar-height":e.appBarHeight}})},b=[],_=n(9582),x=n(4886),w=n(4127),Z=n(266),S=n(2118),C=n(9223),B=n(8224),z=n(5808),M=n(4525),O=n(5200),T=n(9608),q=n(9422),F=n(1713),Q=n(7808),$=function(){var e=this,t=e._self._c;return t(S.Z,{staticClass:"pa-0 fill-height"},[t(F.Z,{staticClass:"no-gutters elevation-4"},[t(Z.Z,{staticClass:"flex-grow-1 flex-shrink-0",attrs:{cols:"auto"}},[t(q.Z,{staticClass:"overflow-y-hidden"},[t(_.Z,{staticClass:"d-flex flex-column",style:{height:`calc(100vh - ${e.appBarHeight}px)`},attrs:{flat:""}},[t(x.ZB,{class:"flex-grow-1 overflow-y-auto "+e.scrollbarTheme},[e._l(e.messages,(function(n,i){return[t("div",{class:{"d-flex flex-row-reverse":n.isUser}},[t(T.Z,{attrs:{"offset-y":""},scopedSlots:e._u([{key:"activator",fn:function({on:i}){return[t(B.Z,{scopedSlots:e._u([{key:"default",fn:function({hover:a}){return[t(w.Z,e._g({staticClass:"pa-4 mb-2",staticStyle:{height:"auto","white-space":"normal"},attrs:{color:n.isUser?"primary":"red",dark:""}},i),[e._v(" "+e._s(n.content)+" "),t("sub",{staticClass:"ml-2",staticStyle:{"font-size":"0.5rem"}},[e._v(" "+e._s(n.created_at)+" ")]),a?t(r.Z,{attrs:{small:""}},[e._v("mdi-chevron-down")]):e._e()],1)]}}],null,!0)})]}}],null,!0)},[t(z.Z,[t(M.Z,[t(O.V9,[e._v("delete")])],1)],1)],1)],1)]})),t("transition",{attrs:{name:"fade"}},[e.waitingForAnswer?t(w.Z,{staticClass:"pa-4 mb-2 d-flex justify-center",staticStyle:{height:"auto","white-space":"normal",width:"70px"},attrs:{color:"red",dark:""}},[t("div",{staticClass:"dot-typing"})]):e._e()],1)],2),t(C.Z),t(x.ZB,{staticClass:"flex-shrink-1"},[t(Q.Z,{attrs:{label:"Mesaj",type:"text","no-details":"",outlined:"","append-outer-icon":"mdi-send","hide-details":""},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.sendMessage.apply(null,arguments)},"click:append-outer":e.sendMessage},model:{value:e.messageForm.content,callback:function(t){e.$set(e.messageForm,"content",t)},expression:"messageForm.content"}})],1)],1)],1)],1)],1)],1)},j=[],A=(n(7658),n(594)),H=n(9367),U={name:"MetubotChat",props:{appBarHeight:Number},data(){return{messages:[],messageForm:{content:"",isUser:!0,created_at:"11:11am"},waitingForAnswer:!0,socketIoSocket:null}},mounted(){this.socketIoSocket=(0,H.io)(),this.socketIoSocket.on("chat answer",(e=>{this.waitingForAnswer=!1,""===e&&(e="Sualinize maalesef mütenasip bir yanıt bulamamaktayım. Başka sorunuz varsa lütfen sakınmayınız."),this.messages.push({content:e,isUser:!1,created_at:this.getClock()})}))},methods:{sendMessageToServer(){A.Z.post("/",{question:this.chatMessage})},getClock(){let e=new Date,t=e.getHours(),n=e.getMinutes();return`${t}:${n}`},sendMessage(){""===this.messageForm.content||this.waitingForAnswer||(this.messageForm.created_at=this.getClock(),this.messages.push(this.messageForm),this.socketIoSocket.emit("chat question",this.messageForm.content),this.messageForm={content:"",isUser:!0,created_at:null},this.waitingForAnswer=!0)}},computed:{scrollbarTheme(){return this.$vuetify.theme.dark?"dark-scrollbar":"light-scrollbar"}}},E=U,P=(0,p.Z)(E,$,j,!1,null,"132ce5e0",null),I=P.exports,Y={name:"Home",props:{appBarHeight:Number},components:{MetubotChat:I}},L=Y,N=(0,p.Z)(L,k,b,!1,null,"4b1846f1",null),V=N.exports,D=function(){var e=this,t=e._self._c;return t("div",[t(S.Z,{staticClass:"pa-0 fill-height"},[t(F.Z,[t(Z.Z,[t("metubot-asked-questions",{staticClass:"mt-5"})],1)],1)],1)],1)},W=[],G=n(5163),J=function(){var e=this,t=e._self._c;return t(_.Z,[t(x.EB,[e._v(" Sorulan Sorular "),t(u.Z),t(Q.Z,{attrs:{"append-icon":"mdi-magnify",label:"Arama"},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}})],1),t(G.Z,{attrs:{headers:e.headers,items:e.questions,search:e.search,"items-per-page":5,"items-per-page-text":"hl","no-results-text":"Sonuç bulunamadı.","no-data-text":"Soru bulunmamaktadır.","footer-props":{"items-per-page-text":"Sayfa başı gösterilecek soru sayısı:"}},scopedSlots:e._u([{key:"footer.page-text",fn:function(t){return[e._v(" "+e._s(t.pageStart)+" - "+e._s(t.pageStop)+" / "+e._s(t.itemsLength)+" ")]}}],null,!0)})],1)},K=[],R={name:"MetubotAskedQuestions",data(){return{search:"",questions:[{question:"Bugün ne yiyeceğiz?",matchedQuestion:"Bugün pilav üstü odtü kavurma yiyeceğiz.",similarity:.8},{question:"Şifremi nasıl öğrenebilirim?",matchedQuestion:"Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",similarity:.6},{question:"Bugün ne yiyeceğiz?",matchedQuestion:"Bugün pilav üstü odtü kavurma yiyeceğiz.",similarity:.8},{question:"Şifremi nasıl öğrenebilirim?",matchedQuestion:"Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",similarity:.6},{question:"Bugün ne yiyeceğiz?",matchedQuestion:"Bugün pilav üstü odtü kavurma yiyeceğiz.",similarity:.8},{question:"Şifremi nasıl öğrenebilirim?",matchedQuestion:"Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",similarity:.6},{question:"Bugün ne yiyeceğiz?",matchedQuestion:"Bugün pilav üstü odtü kavurma yiyeceğiz.",similarity:.8},{question:"Şifremi nasıl öğrenebilirim?",matchedQuestion:"Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",similarity:.6}],headers:[{text:"Sorulan Soru",align:"start",sortable:!0,value:"question"},{text:"Eşleşen Soru",value:"matchedQuestion"},{text:"Benzerlik",value:"similarity"}]}}},X=R,ee=(0,p.Z)(X,J,K,!1,null,"1b65185d",null),te=ee.exports,ne={name:"AdminView",components:{MetubotAskedQuestions:te}},ie=ne,ae=(0,p.Z)(ie,D,W,!1,null,null,null),se=ae.exports;i["default"].use(v.ZP);const re=[{path:"/",name:"metubot",component:V,meta:{title:"METUBOT"}},{path:"/yonetim",name:"admin",component:se,meta:{title:"METUBOT Yönetim"}}],oe=new v.ZP({routes:re});var le=oe,ue=n(707),ce=n.n(ue);n(8556);i["default"].config.productionTip=!1,i["default"].use(ce()),new i["default"]({router:le,vuetify:new(ce())({theme:{dark:!0}}),render:e=>e(y)}).$mount("#app")},7309:function(e,t,n){e.exports=n.p+"img/metubot-logo.828f8f1b.png"}},t={};function n(i){var a=t[i];if(void 0!==a)return a.exports;var s=t[i]={exports:{}};return e[i].call(s.exports,s,s.exports,n),s.exports}n.m=e,function(){var e=[];n.O=function(t,i,a,s){if(!i){var r=1/0;for(c=0;c<e.length;c++){i=e[c][0],a=e[c][1],s=e[c][2];for(var o=!0,l=0;l<i.length;l++)(!1&s||r>=s)&&Object.keys(n.O).every((function(e){return n.O[e](i[l])}))?i.splice(l--,1):(o=!1,s<r&&(r=s));if(o){e.splice(c--,1);var u=a();void 0!==u&&(t=u)}}return t}s=s||0;for(var c=e.length;c>0&&e[c-1][2]>s;c--)e[c]=e[c-1];e[c]=[i,a,s]}}(),function(){n.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return n.d(t,{a:t}),t}}(),function(){n.d=function(e,t){for(var i in t)n.o(t,i)&&!n.o(e,i)&&Object.defineProperty(e,i,{enumerable:!0,get:t[i]})}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){n.p="/"}(),function(){var e={143:0};n.O.j=function(t){return 0===e[t]};var t=function(t,i){var a,s,r=i[0],o=i[1],l=i[2],u=0;if(r.some((function(t){return 0!==e[t]}))){for(a in o)n.o(o,a)&&(n.m[a]=o[a]);if(l)var c=l(n)}for(t&&t(i);u<r.length;u++)s=r[u],n.o(e,s)&&e[s]&&e[s][0](),e[s]=0;return n.O(c)},i=self["webpackChunkmetubot"]=self["webpackChunkmetubot"]||[];i.forEach(t.bind(null,0)),i.push=t.bind(null,i.push.bind(i))}();var i=n.O(void 0,[998],(function(){return n(7592)}));i=n.O(i)})();
//# sourceMappingURL=app.45e5bef3.js.map