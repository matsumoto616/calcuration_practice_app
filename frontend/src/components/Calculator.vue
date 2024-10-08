<template>
    <div id="app">
      <h1>計算アプリ</h1>
      <label for="a">A:</label>
      <input v-model="a" type="number" />
      <label for="b">B:</label>
      <input v-model="b" type="number" />
      <button @click="calculate">計算</button>
      <p>結果: {{ result }}</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        a: 0,
        b: 0,
        result: null,
      };
    },
    methods: {
      calculate() {
        axios
          .post("http://localhost:5000/calculate", { a: this.a, b: this.b })
          .then((response) => {
            this.result = response.data.result;
          })
          .catch((error) => {
            console.error("エラーが発生しました", error);
          });
      },
    },
  };
  </script>
  