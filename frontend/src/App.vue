<template>
  <div id="app">
    <h1>九九の練習アプリ</h1>

    <!-- ログイン/アカウント作成フォーム -->
    <div v-if="!loggedIn">
      <input v-model="username" placeholder="アカウント名を入力" />
      <button @click="createAccount">アカウント作成</button>
      <button @click="login">ログイン</button>
      <p v-if="errorMessage">{{ errorMessage }}</p>
    </div>

    <!-- 練習の開始/終了 -->
    <div v-if="loggedIn && !isTraining">
      <p>アカウント名: {{ username }}</p>
      <button @click="startTraining">練習開始</button>
    </div>

    <!-- 練習中の表示 -->
    <div v-if="isTraining">
      <p>アカウント名: {{ username }}</p>
      <div>
        <label>
          <input type="radio" v-model="mode" value="multiplication" @change="fetchQuestion" checked> 掛け算モード
        </label>
        <label>
          <input type="radio" v-model="mode" value="division" @change="fetchQuestion"> 割り算モード
        </label>
      </div>

      <p>問題: {{ question }}</p>
      <input v-model="userAnswer" type="number" placeholder="答えを入力" />
      <button @click="submitAnswer" :disabled="!userAnswer">送信</button>
      <div class="feedback-container">
        <p v-if="feedback">{{ feedback }}</p>
        <p v-if="elapsedTime">解答時間: {{ elapsedTime }} 秒</p>
      </div>
      <button @click="fetchQuestion">次の問題</button>

      <button @click="endTraining">練習終了</button>
    </div>

    <!-- 統計表示ボタン -->
    <div v-if="loggedIn">
      <button @click="showStatistics">統計を表示</button>
    </div>

    <!-- グラフ表示エリア -->
    <canvas id="statistics-chart" v-if="chartData"></canvas>
  </div>
</template>

<script>
import axios from 'axios';
import { Chart } from 'chart.js';

export default {
  data() {
    return {
      username: '',
      userId: null,
      mode: 'multiplication',
      question: '',
      correctAnswer: null,
      userAnswer: '',
      feedback: '',
      startTime: 0,
      endTime: 0,
      elapsedTime: 0,
      loggedIn: false,
      isTraining: false,  // 練習の状態を管理
      errorMessage: '',
      chartData: null,  // グラフ表示用データ
    };
  },
  methods: {
    async createAccount() {
      try {
        const response = await axios.post('http://localhost:5000/create_account', { username: this.username });
        this.userId = response.data.user_id;
        this.loggedIn = true;
      } catch (error) {
        this.errorMessage = error.response.data.message;
      }
    },
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/login', { username: this.username });
        this.userId = response.data.user_id;
        this.loggedIn = true;
      } catch (error) {
        this.errorMessage = error.response.data.message;
      }
    },
    startTraining() {
      this.isTraining = true;
      this.fetchQuestion();  // 練習開始時に最初の問題を取得
    },
    endTraining() {
      this.isTraining = false;  // 練習を終了
      this.resetState();  // 状態をリセット
    },
    resetState() {
      this.question = '';
      this.correctAnswer = null;
      this.userAnswer = '';
      this.feedback = '';
      this.elapsedTime = 0;
    },
    async fetchQuestion() {
      this.userAnswer = '';
      this.feedback = '';
      this.elapsedTime = 0;
      this.startTime = Date.now(); // 時間計測を開始

      try {
        const response = await axios.post('http://localhost:5000/generate', {
          mode: this.mode,
        });
        this.question = response.data.question;
        this.correctAnswer = response.data.correct_answer;
      } catch (error) {
        console.error('問題の取得に失敗しました', error);
      }
    },
    async submitAnswer() {
      this.endTime = Date.now();
      this.elapsedTime = ((this.endTime - this.startTime) / 1000).toFixed(2); // 経過時間を計算

      try {
        const response = await axios.post('http://localhost:5000/check', {
          user_id: this.userId,
          userAnswer: this.userAnswer,
          correctAnswer: this.correctAnswer,
          question: this.question,
          time_taken: this.elapsedTime,
        });
        if (response.data.result) {
          this.feedback = '正解です！';
        } else {
          this.feedback = `不正解。正しい答えは ${response.data.correct_answer} です。`;
        }
      } catch (error) {
        console.error('解答チェックに失敗しました', error);
      }
    },
    // 統計を取得してグラフ表示
    async showStatistics() {
      try {
        const response = await axios.get('http://localhost:5000/get_statistics');
        this.chartData = response.data;
        this.renderChart();
      } catch (error) {
        console.error('統計データの取得に失敗しました', error);
      }
    },
    renderChart() {
      const ctx = document.getElementById('statistics-chart').getContext('2d');

      const dates = this.chartData.map(item => item.date);
      const correctRatesMultiplication = this.chartData.filter(item => item.mode === 'multiplication').map(item => item.average_correct_rate);
      const correctRatesDivision = this.chartData.filter(item => item.mode === 'division').map(item => item.average_correct_rate);
      const timesMultiplication = this.chartData.filter(item => item.mode === 'multiplication').map(item => item.average_time_taken);
      const timesDivision = this.chartData.filter(item => item.mode === 'division').map(item => item.average_time_taken);

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [
            {
              label: '掛け算モード - 正解率 (%)',
              data: correctRatesMultiplication,
              borderColor: 'blue',
              fill: false,
              yAxisID: 'y-axis-1'
            },
            {
              label: '割り算モード - 正解率 (%)',
              data: correctRatesDivision,
              borderColor: 'green',
              fill: false,
              yAxisID: 'y-axis-1'
            },
            {
              label: '掛け算モード - 平均解答時間 (秒)',
              data: timesMultiplication,
              borderColor: 'red',
              fill: false,
              yAxisID: 'y-axis-2'
            },
            {
              label: '割り算モード - 平均解答時間 (秒)',
              data: timesDivision,
              borderColor: 'orange',
              fill: false,
              yAxisID: 'y-axis-2'
            }
          ]
        },
        options: {
          scales: {
            'y-axis-1': {
              type: 'linear',
              position: 'left',
              ticks: {
                callback: function(value) {
                  return value + '%';
                }
              }
            },
            'y-axis-2': {
              type: 'linear',
              position: 'right',
              ticks: {
                callback: function(value) {
                  return value + '秒';
                }
              }
            }
          }
        }
      });
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 50px;
}
input {
  margin-right: 10px;
}
button {
  margin-top: 10px;
}
.feedback-container {
  min-height: 50px; /* フィードバックエリアの高さを固定 */
  margin-top: 10px;
}
canvas {
  max-width: 100%;
  margin-top: 20px;
}
</style>
