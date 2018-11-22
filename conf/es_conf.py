ES_INDEX_URL = '{es_url}' + '/_cat/indices?v'
ES_TYPE_URL = '{es_url}' + "/_mapping?pretty=true"
ES_NODES = 'escuster.vip.xywy.com'
HIVE_SQL_BASE = """
CREATE EXTERNAL TABLE `{table_name}`(
{field_str}
)
STORED BY 
  'org.elasticsearch.hadoop.hive.EsStorageHandler' 
TBLPROPERTIES (
  'es.nodes'='{es_nodes}', 
  'es.index.auto.create'='false', -- true 自动创建索引，false 不自动创建
  'es.resource'='/{index}/{type}/',
  'es.mapping.id' = 'id' -- 设置hive表的id字段对应elasticsearch的_id（唯一索引，相当于mysql的主键，灌入数据时相同的id表示更新数据）
)"""

if __name__ == '__main__':
    import requests
    import json
    response = requests.get(ES_INDEX_URL,
                            headers={'Content-Type':'application/json'}
                            )
    print(response.text)
    print(type(response.text))
    print(json.loads(response.text))

