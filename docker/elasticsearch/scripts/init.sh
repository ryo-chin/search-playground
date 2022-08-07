current_dir=`dirname $0`

curl -X DELETE 'http://localhost:9200/ng_word?pretty'
curl -X PUT 'http://localhost:9200/ng_word?include_type_name=true&pretty=true' -H 'Content-Type: application/json' -d @${current_dir}/../schema/ng_word.json
