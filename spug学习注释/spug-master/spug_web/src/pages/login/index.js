/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import {Form, Input, Icon, Button, Tabs, Modal} from 'antd';
import styles from './login.module.css';
import history from 'libs/history';
import {http, updatePermissions} from 'libs';
import logo from 'layout/logo-spug-txt.png';
import envStore from 'pages/config/environment/store';
import appStore from 'pages/config/app/store';
import requestStore from 'pages/deploy/request/store';
import execStore from 'pages/exec/task/store';
import hostStore from 'pages/host/store';

class LoginIndex extends React.Component {  //定义class组件LoginIndex，并需要继承React.Component组件
  constructor(props) {  //调用constructor函数
    super(props);  //super代表父类的构造函数，继续父类函数。
    this.state = {  //赋值
      loading: false,
      loginType: 'default'
    }
  }

  componentDidMount() {  //componentDidMount() 会在组件挂载后（插入 DOM 树中）立即调用。依赖于 DOM 节点的初始化应该放在这里。如需通过网络请求获取数据，此处是实例化请求的好地方。
    envStore.records = []; //初始化环境对象
    appStore.records = []; //初始化管理权限模块
    requestStore.records = []; //初始化返回权限模块
    requestStore.deploys = []; //初始化开发权限模块
    hostStore.records = [];   //初始化主机权限模块
    execStore.hosts = [];     //初始化执行权限模块
  }

  handleSubmit = () => {    //定义点击事件函数
    this.props.form.validateFields((err, formData) => {  //校验表单数据
      if (!err) {
        this.setState({loading: true}); //定义loading状态
        formData['type'] = this.state.loginType; //定义登陆类型
        http.post('/api/account/login/', formData) //向后端请求数据验证
          .then(data => {  //定义data函数，将后端返回数据保存为data
            if (!data['has_real_ip']) {  //检查是否获取到真实ip
              Modal.warning({
                title: '安全警告',
                className: styles.tips,
                content: <div>
                  未能获取到客户端的真实IP，无法提供基于请求来源IP的合法性验证，详细信息请参考
                  <a target="_blank" href="https://spug.dev" rel="noopener noreferrer">官方文档</a>。
                </div>,
                onOk: () => this.doLogin(data) //重置函数事件
              })
            } else {
              this.doLogin(data)  //调用函数
            }
          }, () => this.setState({loading: false})) //设置loading状态为false
      }
    })
  };

  doLogin = (data) => {  //定义登陆函数doLogin
    localStorage.setItem('token', data['access_token']);  //从返回数据中提取各种信息
    localStorage.setItem('nickname', data['nickname']);
    localStorage.setItem('is_supper', data['is_supper']);
    localStorage.setItem('permissions', JSON.stringify(data['permissions']));
    localStorage.setItem('host_perms', JSON.stringify(data['host_perms']));
    updatePermissions(data['is_supper'], data['host_perms'], data['permissions']); //调用libs下函数，更新用户权限和主机权限。
    if (history.location.state && history.location.state['from']) {
      history.push(history.location.state['from']) //查找历史记录，并返回到上次登陆点。
    } else {
      history.push('/welcome/index') //进入主页面
    }
  };

  render() {  //render函数，生成web显示页面
    const {getFieldDecorator} = this.props.form; //定义变量，并初始化
    return ( //返回页面内容
      <div className={styles.container}>
        <div className={styles.titleContainer}>
          <div><img className={styles.logo} src={logo} alt="logo"/></div>
          <div className={styles.desc}>灵活、强大、功能全面的开源运维平台</div>
        </div>
        <div className={styles.formContainer}>
          <Tabs classNam={styles.tabs} onTabClick={e => this.setState({loginType: e})}>
            <Tabs.TabPane tab="普通登录" key="default"/>
            <Tabs.TabPane tab="LDAP登录" key="ldap"/>
          </Tabs>
          <Form>
            <Form.Item className={styles.formItem}>
              {getFieldDecorator('username', {rules: [{required: true, message: '请输入账户'}]})(
                <Input
                  size="large"
                  autoComplete="off"
                  placeholder="请输入账户"
                  prefix={<Icon type="user" className={styles.icon}/>}/>
              )}
            </Form.Item>
            <Form.Item className={styles.formItem}>
              {getFieldDecorator('password', {rules: [{required: true, message: '请输入密码'}]})(
                <Input
                  size="large"
                  type="password"
                  autoComplete="off"
                  placeholder="请输入密码"
                  onPressEnter={this.handleSubmit} \\回车执行函数
                  prefix={<Icon type="lock" className={styles.icon}/>}/>
              )}
            </Form.Item>
          </Form>

          <Button
            block
            size="large"
            type="primary"
            className={styles.button}
            loading={this.state.loading}
            onClick={this.handleSubmit}>登录</Button>
        </div>

        <div className={styles.footerZone}>
          <div className={styles.linksZone}>
            <a className={styles.links} title="官网" href="https://www.spug.dev"  target="_blank"
               rel="noopener noreferrer">官网</a>
            <a className={styles.links} title="Github" href="https://github.com/openspug/spug"  target="_blank"
               rel="noopener noreferrer"><Icon type="github" /></a>
            <a title="文档" href="https://www.spug.dev/docs/about-spug/"  target="_blank"
               rel="noopener noreferrer">文档</a>
          </div>
          <div style={{color: 'rgba(0, 0, 0, .45)'}}>Copyright <Icon type="copyright" /> 2020 By OpenSpug</div>
        </div>
      </div>
    )
  }
}

export default Form.create()(LoginIndex)
