宕机监控(iplive)  
=============================
-
<br/>
**错误代码及其解释**  <br/>

```
1001 Unknow Error
1002 Lack of Param
1003 Param Error(scan interval not valid)
1004 Token not right
1005 Not found valid function for app name
```

## operate_monitor(add&update)
**A brief description:**  <br/>
`add a group of monitor target into iplive`  <br/>
**Request url**  <br/>
`http://43.247.89.4:6003/operate_monitor`  <br/>

**Method**  <br/>
`POST`  <br/>

**Request params:**  <br/>
<table>
<tr>
<td>param</td><td>Required</td><td>Type</td><td>Description</td>
</tr>

<tr>
<td>app_name</td><td>Yes</td><td>String</td><td>针对于不通的项目的一个唯一识别</td>
</tr>

<tr>
<td>group_id</td><td>Yes</td><td>int</td><td>组ID</td>
</tr>

<tr>
<td>record_ids</td><td>Yes</td><td>int</td><td>记录的id </td>
</tr>

<tr>
<td>ips</td><td>Yes</td><td>int</td><td>主IP 多个之间用:隔开  我这里不区分主ip和备用ip</td>
</tr>

<tr>
<td>level</td><td>No</td><td>int</td><td>用户的等级。能够决定享用的节点数量 默认是0</td>
</tr>

<tr>
<td>protocol</td><td>No</td><td>String</td><td>对目标检测的协议 默认http</td>
</tr>

<tr>
<td>port</td><td>No</td><td>int</td><td>检测端口 http默认80 https默认443</td>
</tr>

<tr>
<td>path</td><td>No</td><td>String</td><td>网页路径</td>
</tr>


<tr>
<td>domain</td><td>No</td><td>String</td><td>请求的时候所携带的Host头</td>
</tr>

<tr>
<td>cookies</td><td>No</td><td>String</td><td>访问时可携带的cookies</td>
</tr>

<tr>
<td>http_code</td><td>No</td><td>int(string)</td><td>用户认为正确的httpcode</td>
</tr>

<tr>
<td>interval</td><td>No</td><td>int</td><td>探测的时间间隔 默认60s</td>
</tr>

<tr>
<td>timeout</td><td>No</td><td>int</td><td>节点访问的超时时间(预留字段) 默认3秒</td>
</tr>

<tr>
<td>retry_count</td><td>No</td><td>int</td><td>节点访问失败的重试次数(预留字段) 默认0次</td>
</tr>

<tr>
<td>node_ips</td><td>No</td><td>String</td><td>用户可选的节点IP(作为扩展字段 一期不做)</td>
</tr>
</table>

## update_monitor
**A brief description:**  <br/>

```plain text
update IP of a certain record
```

**Request url**  <br/>
`http://43.247.89.4:6003/update_monitor`  <br/>

**Method**  <br/>
`POST`  <br/>

**Request params:**  <br/>

<table>
<tr>
<td>param</td><td>Required</td><td>Type</td><td>Description</td>
</tr>


<tr>
<td>group_id</td><td>Yes</td><td>int</td><td>组ID</td>
</tr>
<tr>
<td>app_name</td><td>Yes</td><td>int</td><td>应用的名字</td>
</tr>
<tr>
<td>record_id</td><td>Yes</td><td>int</td><td>记录的名字</td>
</tr>
<tr>
<td>ip</td><td>Yes</td><td>string</td><td>修改之后的ip</td>
</tr>

</table>


## stop_monitor
**A brief description:**  <br/>

```plain text
stop monitor
```

**Request url**  <br/>
`http://43.247.89.4:6003/stop_monitor`  <br/>

**Method**  <br/>
`POST`  <br/>

**Request params:**  <br/>

<table>
<tr>
<td>param</td><td>Required</td><td>Type</td><td>Description</td>
</tr>


<tr>
<td>group_id</td><td>Yes</td><td>int</td><td>组ID</td>
</tr>
<tr>
<td>app_name</td><td>Yes</td><td>int</td><td>应用的名字</td>
</tr>

</table>

## add_node
**A brief description:**  <br/>

```plain text
add new client node
```

**Request url**  <br/>
`http://43.247.89.4:6003/add_node`  <br/>

**Method**  <br/>
`POST`  <br/>

**Request params:**  <br/>

<table>
<tr>
<td>param</td><td>Required</td><td>Type</td><td>Description</td>
</tr>


<tr>
<td>node_ip</td><td>Yes</td><td>string</td><td>节点的ip地址</td>
</tr>
<tr>
<td>passwd</td><td>Yes</td><td>string</td><td>密码</td>
</tr>

</table>

## deal
**A brief description:**  <br/>

```plain text
deal with detect result of nodes
```

**Request url**  <br/>
`http://43.247.89.4:6003/deal`  <br/>

**Method**  <br/>
`POST`  <br/>

**Request params:**  <br/>

<table>
<tr>
<td>param</td><td>Required</td><td>Type</td><td>Description</td>
</tr>

<tr>
<td>timestamp</td><td>Yes</td><td>int</td><td>时间戳</td>
</tr>

<tr>
<td>data</td><td>Yes</td><td>json</td><td>[{'server_id': 1, 'timestamp': '', 'last_status': '200', 'res_time': '5'}]</td>
</tr>


</table>




## call\_back\_to\_php
**A brief description:**  <br/>

```plain text
Send result from server to php
```

**Method**  <br/>
`POST`  <br/>

**Request params:**  <br/>

<table>
<tr>
<td>param</td><td>Required</td><td>Type</td><td>Description</td>
</tr>

<tr>
<td>group_id</td><td>Yes</td><td>int</td><td>组ID</td>
</tr>

<tr>
<td>timestamp</td><td>Yes</td><td>int</td><td>标识探测的时间</td>
</tr>

<tr>
<td>result</td><td>Yes</td><td>json</td><td>[{'record_id': '1', 'status': '1', 'res_time': 5}]</td>
</tr>


</table>

