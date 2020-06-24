<template>
 <div class="home">
  <div>
 <el-button type="primary" class="mt_0 ml_1em  bg_gray_777" @click="searchClick()">查询</el-button>
 <el-button type="primary" class="mt_0 ml_1em  bg_gray_777" @click="exportClick()">导出</el-button>
 </div>
 <div>
   <el-row>
       <el-table :data="bookList" style="width: 100%" border>
         <el-table-column prop="id" label="编号" min-width="100">
           <template scope="scope"> {{ scope.row.id }} </template>
         </el-table-column>
         <el-table-column prop="book_name" label="书名" min-width="100">
           <template scope="scope"> {{ scope.row.book_name }} </template>
         </el-table-column>
         <el-table-column prop="add_time" label="添加时间" min-width="100">
           <template scope="scope"> {{ scope.row.add_time }} </template>
         </el-table-column>
       </el-table>
   </el-row>
 </div>
 </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      bookList: []
    }
  },
  methods: {
    searchClick:function () {
     this.$http.get('http://127.0.0.1:8000/api/show_books')
       .then((response) => {
         var res = JSON.parse(response.bodyText)
         console.log(res)
         if (res.error_num === 0) {
           this.bookList = res['list']
         } else {
           this.$message.error('查询书籍失败')
           console.log(res['msg'])
         }
       })
    },
    exportClick:function () {
      require.ensure([], () => {
      　　　　　　　　const { export_json_to_excel } = require('../ven/Export2Excel');
      　　　　　　　　const tHeader = ['编号', '书名','增加时间']; //对应表格输出的title
      　　　　　　　　const filterVal = ['id', 'book_name','add_time']; // 对应表格输出的数据
      　　　　　　　　const list = this.bookList;
      　　　　　　　　const data = this.formatJson(filterVal,list);
      　　　　　　　　export_json_to_excel(tHeader, data, '列表excel'); //对应下载文件的名字
                   console.log("success")
      　　　　　　})
      　　　　},
     formatJson(filterVal, jsonData) {
      　return jsonData.map(v => filterVal.map(j => v[j]))
        },
    }
}
</script>

<style>
</style>
