<template>
  <div class="login">
    <div class="login-con">
      <Card icon="log-in" title="欢迎登录" :bordered="false">
        <div class="form-con">
          <LoginForm v-on:listenChildEvent="checkLogin"/>
          <p class="login-tip">输入任意用户名和密码即可</p>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import LoginForm from '@/components/Login_form.vue'
import axios from "axios"

export default {
  name: 'Login',
  components: {
    LoginForm
  },

  methods: {
      checkLogin: function(data){
        console.log(data)

        var that = this
        var parms = new URLSearchParams()

        parms.append('username', data.username)
        parms.append('password', data.password)
        axios.post('http://localhost:5000/api/login', parms).then(function (res) {
        if (res.data.isLogin == '-1') {
          alert('用户名或密码错误')
        } else {
          sessionStorage.setItem('userInfo', JSON.stringify(res.data))
          that.$router.push({ path: '/menu' })
        }
      })

      }

  },


}
</script>
