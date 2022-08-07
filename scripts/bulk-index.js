const { Client } = require('@elastic/elasticsearch');
const client = new Client({ node: 'http://localhost:9200' });

async function bulkIndex() {
  const response = await client.index({ index: 'ng_word', body: { word: 'NGワード', word_type: 'ngw' } });
  console.log(response)
}

module.exports = bulkIndex;
