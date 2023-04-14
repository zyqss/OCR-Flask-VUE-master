<!--形成虚拟节点，也就是末班所在位置-->
<template>
  <div id="app">
  <el-container >
      <el-header>
        <app-header></app-header>
      </el-header>
      <el-container>
        <el-aside>
          <app-main></app-main>
        </el-aside>
        <el-main>
        <app-content></app-content>
        <app-footer></app-footer>
        </el-main>
      </el-container>
  </el-container>

    <!--<app-header></app-header>
    <app-content></app-content>
    <app-footer></app-footer>-->

  </div>
</template>

<!--写组件代码-->
<script>
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Content from "@/components/Content";
import Main from "@/components/Main";
export default {
  name: "ID",
  data() {
    return {};
  },
  components: {
    "app-header": Header,
    "app-footer": Footer,
    "app-content": Content,
    "app-main": Main,
  },
  methods: {},
};
</script>

<style scope="this api replaced by slot-scope in 2.5.0+">
</style>

