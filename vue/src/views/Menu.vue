<!--形成虚拟节点，也就是末班所在位置-->
<!--<template>
  <div id="app">
  <el-container >
      <el-aside>
        <app-main></app-main>
      </el-aside>
      <el-main>
        <app-header></app-header>
        <app-main_content></app-main_content>
        <app-footer></app-footer>
      </el-main>
  </el-container>

    <!--<app-header></app-header>
    <app-content></app-content>
    <app-footer></app-footer>-->

  </div>
</template>-->

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
        <app-main_content></app-main_content>
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
import Main_Content from "@/components/Main_Content";
import Main from "@/components/Main";
export default {
  name: "Fapiao",
  data() {
    return {};
  },
  components: {
    "app-header": Header,
    "app-footer": Footer,
    "app-main_content": Main_Content,
    "app-main": Main,
  },
  methods: {},
};
</script>

<style scope="this api replaced by slot-scope in 2.5.0+">
</style>

