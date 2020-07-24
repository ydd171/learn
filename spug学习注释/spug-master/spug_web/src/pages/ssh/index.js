/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { Button } from 'antd';
import { Terminal } from 'xterm';  //xterm标准模拟终端
import { FitAddon } from 'xterm-addon-fit'; //使终端适用与包含元素
import FileManager from './FileManager';
import { http } from 'libs';
import 'xterm/css/xterm.css';
import styles from './index.module.css';


class WebSSH extends React.Component {  //创建webssh组件
  constructor(props) {  //创建props属性
    super(props);  //声明props参数父类，与React.Component配套使用
    this.id = props.match.params.id; //初始化参数值
    this.token = localStorage.getItem('token');
    this.socket = null;
    this.term = new Terminal();
    this.container = null;
    this.input = null;
    this.state = {
      visible: false,
      uploading: false,
      managerDisabled: true,
      host: {},
      percent: 0
    }
  }

  componentDidMount() {  //定义更新完组件后立即调用函数钩子
    this._fetch(); //向api请求连接函数
    const fitPlugin = new FitAddon(); //定义终端显示类型
    this.term.loadAddon(fitPlugin);  //应用显示类型
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';  //指定跳转连接，如果使https使用wss连接，else使用ws连接。
    this.socket = new WebSocket(`${protocol}//${window.location.host}/api/ws/ssh/${this.token}/${this.id}/`); //启用websock连接。
    this.socket.onmessage = e => this._read_as_text(e.data); //定义显示信息
    this.socket.onopen = () => {  //定义窗口开启状态下的函数。
      this.term.open(this.container);
      this.term.focus();
      fitPlugin.fit();
    };
    this.socket.onclose = e => { //定义窗口连接关闭状态下的函数。
      if (e.code === 3333) {
        window.location.href = "about:blank";
        window.close()
      } else {
        setTimeout(() => this.term.write('\r\nConnection is closed.\r\n'), 200) //定义超时时间
      }
    };
    this.term.onData(data => this.socket.send(JSON.stringify({data}))); //时间
    this.term.onResize(({cols, rows}) => {
      this.socket.send(JSON.stringify({resize: [cols, rows]}))  //输入大小
    });
    window.onresize = () => fitPlugin.fit()      //输出大小
  }

  _read_as_text = (data) => {  //输出显示
    const reader = new window.FileReader();
    reader.onload = () => this.term.write(reader.result);
    reader.readAsText(data, 'utf-8')
  };

  handleShow = () => {  //状态更新
    this.setState({visible: !this.state.visible})
  };

  _fetch = () => {  //向api请求连接
    http.get(`/api/host/?id=${this.id}`)
      .then(res => {
        document.title = res.name;
        this.setState({host: res, managerDisabled: false})
      })
  };

  render() {  //定义显示界面
    const {host, visible, managerDisabled} = this.state;
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <div>{host.name} | {host.username}@{host.hostname}:{host.port}</div>
          <Button disabled={managerDisabled} type="primary" icon="folder-open" onClick={this.handleShow}>文件管理器</Button>
        </div>
        <div className={styles.terminal}>
          <div ref={ref => this.container = ref}/>
        </div>
        <FileManager id={this.id} visible={visible} onClose={this.handleShow} />
      </div>
    )
  }
}

export default WebSSH