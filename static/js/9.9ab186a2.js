(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[9],{"39c9":function(a,e,s){"use strict";s.r(e);var t=function(){var a=this,e=a.$createElement,s=a._self._c||e;return s("q-page",[s("div",{staticClass:"row q-pa-xl"},[s("div",{staticClass:"col-5"},[s("q-card",{attrs:{flat:""}},[s("q-card-section",[s("h6",{staticClass:"q-ma-none q-pa-none"},[a._v("Form Tambah Data Guru")])]),s("q-card-section",[s("q-form",{ref:"form",on:{submit:a.save}},[s("q-input",{staticClass:"q-mb-md",attrs:{label:"NIP",filled:"",rules:a.rules.nip},model:{value:a.nip,callback:function(e){a.nip=e},expression:"nip"}}),s("q-input",{staticClass:"q-mb-md",attrs:{label:"Nama Guru",filled:"",rules:a.rules.nama},model:{value:a.nama,callback:function(e){a.nama=e},expression:"nama"}}),s("div",{staticClass:"q-mb-md"},[s("label",[a._v("Jenis Kelamin")]),s("div",{staticClass:"q-gutter-sm"},[s("q-radio",{attrs:{val:"Laki",label:"Laki - Laki"},model:{value:a.sex,callback:function(e){a.sex=e},expression:"sex"}}),s("q-radio",{attrs:{val:"Perempuan",label:"Perempuan"},model:{value:a.sex,callback:function(e){a.sex=e},expression:"sex"}})],1)]),s("div",[s("q-btn",{staticClass:"q-mr-md",attrs:{label:"simpan",type:"submit",color:"blue",depressed:""}}),s("q-btn",{attrs:{label:"reset",type:"reset",depressed:""}})],1)],1)],1)],1)],1)])])},i=[],n=(s("e6cf"),s("ded3")),l=s.n(n),r=s("2f62");const o=/^\d+$/;var u={name:"CreateGuru",data:()=>({nama:"",sex:"Laki",nip:"",items:[],errors:null,rules:{nama:[a=>!!a||"Nama harus diisi"],nip:[a=>!!a||"NIP harus diisi",a=>20==a.length||"NIP harus 20 karakter",a=>a.match(o)||"NIP berupa digit"]}}),computed:l()({},Object(r["b"])({user:a=>a.user})),methods:{async save(){const a=this.$refs.form.validate();if(!a)return void alert("data tidak valid");const e={nama:this.nama,nip:this.nip,sex:this.sex,id_app_user:this.user.id};try{this.$q.loading.show({delay:500});const a=await this.$api.post("/guru",e);console.log(a.data),this.$q.notify({message:"sukses menambah data guru",color:"green"}),this.$router.back()}catch(s){console.log(s),this.errors="terjadi kesalahan",this.$q.notify({message:"gagal menambah data guru",color:"red"})}finally{this.$q.loading.hide()}}}},c=u,d=s("2877"),m=s("9989"),p=s("f09f"),b=s("a370"),h=s("0378"),f=s("27f9"),q=s("3786"),v=s("9c40"),g=s("eebe"),k=s.n(g),x=Object(d["a"])(c,t,i,!1,null,null,null);e["default"]=x.exports;k()(x,"components",{QPage:m["a"],QCard:p["a"],QCardSection:b["a"],QForm:h["a"],QInput:f["a"],QRadio:q["a"],QBtn:v["a"]})}}]);