<!--<template>
  <div class="msgclass">
    {{msg}}
  </div>
</template>

<script>
  export default { //配置对象（与vue一致）
    name: 'HelloWorld.vue',
    data (){//data可以写对象也可以写函数，但是在这里必须写函数
      return {
        msg:'hello vue component'
      }
    }
  }
</script>

<style >
  .msgclass{
    color: red;
    font-size: 15px;
  }
</style>-->


<template>
  <!-- <router-link to="demo">身份证识别</router-link> -->
  <div>
  <el-button
    type="primary"
    style="margin-left: 35px"
    icon="el-icon-upload"
    class="yingye_bt"
    @click="addRoutes"
  >
    主菜单
  </el-button>

  <el-button
    type="primary"
    style="margin-left: 35px"
    icon="el-icon-upload"
    class="identitycard_bt"
    @click="addRoutes1"
  >
    身份证识别
  </el-button>

  <el-button
    type="primary"
    style="margin-left: 35px"
    icon="el-icon-upload"
    class="yingye_bt"
    @click="addRoutes2"
  >
    发票识别
  </el-button>

  <el-button
    type="primary"
    style="margin-left: 35px"
    icon="el-icon-upload"
    class="fapiao_bt"
    @click="addRoutes3"
  >
    车票识别
  </el-button>

  <el-button
    type="primary"
    style="margin-left: 35px"
    icon="el-icon-upload"
    class="yingye_bt"
    @click="addRoutes4"
  >
    营业执照识别
  </el-button>

  </div>
</template>

<script type="text/javascript">

export default {
  components: {
  },
  name: 'Menu',
  data () {
    // 注意：data即使不需要传数据，也必须return,否则会报错
    return {
     }
  },
  methods: {
    addRoutes () {
      this.$router.push('/menu')
    },
    addRoutes1 () {
      this.$router.push('/identitycard')
    },
    addRoutes2 () {
      this.$router.push('/fapiao')
    },
    addRoutes3 () {
      this.$router.push('/ticket')
    },
    addRoutes4 () {
      this.$router.push('/BusinessLicense')
    },
  },
}
</script>

<style type='text/css'>
.el-button {
  padding: 12px 20px !important;
}
</style>






