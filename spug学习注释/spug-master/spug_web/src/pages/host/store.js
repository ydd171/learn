/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { observable } from "mobx"; //定义淘宝mobx框架
import http from 'libs/http';

class Store {   //初始化数据
  @observable records = [];
  @observable zones = [];
  @observable permRecords = [];
  @observable record = {};
  @observable idMap = {};
  @observable isFetching = false;
  @observable formVisible = false;
  @observable importVisible = false;

  @observable f_name;
  @observable f_zone;
  @observable f_host;

  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/host/')  //向后端请求数据
      .then(({hosts, zones, perms}) => {  //数据提取
        this.records = hosts;
        this.zones = zones;
        this.permRecords = hosts.filter(item => perms.includes(item.id)); //从权限数据中检查是否包含主机id
        for (let item of hosts) { //循环获取hosts
          this.idMap[item.id] = item //给idMap赋值
        }
      })
      .finally(() => this.isFetching = false) //初始化isFetching
  };

  showForm = (info = {}) => { //调用显示form表单函数
    this.formVisible = true;
    this.record = info //显示空数据
  }
}

export default new Store()
