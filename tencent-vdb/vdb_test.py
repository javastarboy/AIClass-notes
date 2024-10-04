import os

import tcvectordb
from tcvectordb.model.collection import Embedding
from tcvectordb.model.collection_view import Embedding
from tcvectordb.model.document import Filter, Document
from tcvectordb.model.document import SearchParams
from tcvectordb.model.enum import FieldType, IndexType, ReadConsistency
from tcvectordb.model.enum import MetricType, EmbeddingModel
from tcvectordb.model.index import Index, FilterIndex
from tcvectordb.model.index import VectorIndex, HNSWParams

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

url = os.getenv('VDB_URL')
username = os.getenv('VDB_USER')
KEY = os.getenv('VDB_KEY')

def create_client():
    client = tcvectordb.VectorDBClient(url=url, username=username,
                                       key=key,
                                       read_consistency=ReadConsistency.EVENTUAL_CONSISTENCY, timeout=30)
    return client


def get_db(database_name):
    # 创建数据库
    client = create_client()
    db1 = client.database(database=database_name)
    # 开启日志
    tcvectordb.debug.DebugEnable = True
    return db1


def create_collection_for_vector(db, name, shard, replicas, description):
    """
    针对直接写入向量创建集合
    1、创建集合之前，需先设计索引结构，指定索引字段。如下示例，创建一个可写入 3 维向量数据存储书籍的集合 book-vector，其书籍信息字段包括： id、vector、bookName，分别对各字段构建索引。有关索引的具体信息，请参见 Index。
        ① 主键索引（Primary Key Index）：固定且必须，对应字段 id，每条数据的唯一标识。并对主键 id 构建 Filter 索引，以便可通过 id 的条件表达式进行特定行的检索。
        ② 向量索引（Vector Index）：固定且必须，对应字段 vector，对向量数据构建索引，指定向量数据的维度、数据存储的索引类型、相似性计算方法及相关索引参数。
        ③ Filter 索引（Filter Index）：需根据检索需求选取可作为条件查询过滤数据的字段。通常，向量数据对应的文本字段，不具有过滤属性，则无需对该字段建立索引，否则，将浪费较大的内存也无实际意义。如下示例，预按书籍的名称过滤数据，对 bookName 字段建立 Filter 索引。
    2、创建集合，免费测试版实例，其分片 shard 只能为 1，副本 replicas 仅能为 0。

    :param description:
    :param replicas:
    :param name:
    :param shard:
    :param db:
    :return:
    """
    index = Index(
        FilterIndex(name='id', field_type=FieldType.String, index_type=IndexType.PRIMARY_KEY),
        VectorIndex(name='vector', dimension=3, index_type=IndexType.HNSW,
                    metric_type=MetricType.COSINE, params=HNSWParams(m=16, efconstruction=200)),
        FilterIndex(name=name, field_type=FieldType.String, index_type=IndexType.FILTER)
    )

    if not name:
        raise "集合名称不能为空"
    if not shard:
        shard = 1
    if not replicas:
        replicas = 0

    coll = db.create_collection(
        name=name,
        shard=shard,
        replicas=replicas,
        description=description,
        index=index
    )
    print(vars(coll))

    return coll


def create_collection_for_text(db, name, shard, replicas, description):
    """
    针对写入文本创建集合
    1、创建集合之前，需先设计索引结构，指定索引字段。如下示例，创建一个可写入 3 维向量数据存储书籍的集合 book-vector，其书籍信息字段包括： id、vector、bookName，分别对各字段构建索引。有关索引的具体信息，请参见 Index。
        ① 主键索引（Primary Key Index）：固定且必须，对应字段 id，每条数据的唯一标识。并对主键 id 构建 Filter 索引，以便可通过 id 的条件表达式进行特定行的检索。
        ② 向量索引（Vector Index）：固定且必须，对应字段 vector，对向量数据构建索引，指定向量数据的维度、数据存储的索引类型、相似性计算方法及相关索引参数。
        ③ Filter 索引（Filter Index）：需根据检索需求选取可作为条件查询过滤数据的字段。通常，向量数据对应的文本字段，不具有过滤属性，则无需对该字段建立索引，否则，将浪费较大的内存也无实际意义。如下示例，预按书籍的名称过滤数据，对 bookName 字段建立 Filter 索引。
    2、创建集合，免费测试版实例，其分片 shard 只能为 1，副本 replicas 仅能为 0。

    :param description:
    :param replicas:
    :param name:
    :param shard:
    :param db:
    :return:
    """
    # 第一步：设计索引字段
    index = Index(
        FilterIndex(name='id', field_type=FieldType.String, index_type=IndexType.PRIMARY_KEY),
        VectorIndex(name='vector', dimension=3, index_type=IndexType.HNSW,
                    metric_type=MetricType.COSINE, params=HNSWParams(m=16, efconstruction=200)),
        FilterIndex(name=name, field_type=FieldType.String, index_type=IndexType.FILTER)
    )

    # 第二步：配置 Embedding 参数
    # 1. 指定文本字段与向量字段，向量字段固定为vector
    # 2. 指定 Embedding 模型，推荐使用 BGE_BASE_ZH。
    ebd = Embedding(vector_field='vector', field='text', model=EmbeddingModel.BGE_BASE_ZH)

    if not name:
        raise "集合名称不能为空"
    if not shard:
        shard = 1
    if not replicas:
        replicas = 0

    # 第三步，创建 Collection
    coll = db.create_collection(
        name=name,
        shard=shard,
        replicas=replicas,
        description=description,
        embedding=ebd,
        index=index
    )
    print(vars(coll))

    return coll


def create_collection_for_file(db, collection_name, description):
    """
    针对文件创建集合【官方教程：https://cloud.tencent.com/document/product/1709/102334】
    1、创建集合之前，需先设计索引结构，指定索引字段。如下示例，创建一个可写入 3 维向量数据存储书籍的集合 book-vector，其书籍信息字段包括： id、vector、bookName，分别对各字段构建索引。有关索引的具体信息，请参见 Index。
        ① 主键索引（Primary Key Index）：固定且必须，对应字段 id，每条数据的唯一标识。并对主键 id 构建 Filter 索引，以便可通过 id 的条件表达式进行特定行的检索。
        ② 向量索引（Vector Index）：固定且必须，对应字段 vector，对向量数据构建索引，指定向量数据的维度、数据存储的索引类型、相似性计算方法及相关索引参数。
        ③ Filter 索引（Filter Index）：需根据检索需求选取可作为条件查询过滤数据的字段。通常，向量数据对应的文本字段，不具有过滤属性，则无需对该字段建立索引，否则，将浪费较大的内存也无实际意义。如下示例，预按书籍的名称过滤数据，对 bookName 字段建立 Filter 索引。
    2、创建集合，免费测试版实例，其分片 shard 只能为 1，副本 replicas 仅能为 0。

    :param description:
    :param collection_name:
    :param db:
    :return:
    """

    # 第一步：设计索引，为文件 meta 信息标量字段 author 配置 Filter 索引
    index = Index()
    index.add(FilterIndex('author', FieldType.String, IndexType.FILTER))
    # 第二步：创建集合视图
    coll_view = db.create_collection_view(name=collection_name,
                                          description=description,
                                          index=index)

    print(vars(coll_view))

    return coll_view


def upsert_by_vector(db, collection_name):
    """
    1、直接写入向量数据并检索
    2、适用于已有自身的向量数据，无需使用腾讯云向量数据库进行数据向量化的场景。
    3、说明
        ① 向量数据库支持动态 Schema，写入数据时可以写入任何字段，无需提前定义，类似 MongoDB。如下示例，page 与 author 为新定义的书籍信息字段。
        ② 创建集合时，并未对 page 与 author 构建 Filter 索引，因此，二者不具有过滤属性，仅 bookName 具有过滤属性。

    :return:
    """
    coll = db.collection(collection_name)
    res = coll.upsert(
        documents=[
            Document(id='0001', vector=[
                0.2123, 0.23, 0.213], author='罗贯中', bookName='三国演义', page=21),
            Document(id='0002', vector=[
                0.2123, 0.22, 0.213], author='吴承恩', bookName='西游记', page=22),
            Document(id='0003', vector=[
                0.2123, 0.21, 0.213], author='曹雪芹', bookName='红楼梦', page=23)
        ]
    )

    return res


def upsert_by_text(db, collection_name):
    """
    1、基于文本信息写入向量数据
    2、适用于已有自身的向量数据，无需使用腾讯云向量数据库进行数据向量化的场景。
    3、说明：
        ① 向量数据库支持动态 Schema，写入数据时可以写入任何字段，无需提前定义，类似 MongoDB。如下示例，page 与 author 为新定义的书籍信息字段。
        ② 创建集合时，并未对 page 与 author 构建 Filter 索引，因此，二者不具有过滤属性，仅 bookName 具有过滤属性。
        ③ 写入数据，可能存在一定延迟。

    :return:
    """
    coll = db.collection(collection_name)
    res = coll.upsert(
        documents=[
            Document(id='0001', text="话说天下大势，分久必合，合久必分。", author='罗贯中', bookName='三国演义', page=21),
            Document(id='0002', text="混沌未分天地乱，茫茫渺渺无人间。", author='吴承恩', bookName='西游记', page=22),
            Document(id='0003', text="甄士隐梦幻识通灵，贾雨村风尘怀闺秀。", author='曹雪芹', bookName='红楼梦', page=23)
        ],
    )


def upsert_by_file(db, collection_name, local_file_path, author):
    """
    1、直接写入向量数据并检索
    3、适用于已有自身的向量数据，无需使用腾讯云向量数据库进行数据向量化的场景。
    :return:
    """
    coll_view = db.collection(collection_name)
    # 上传文件
    # 1. 指定文件在客户端的存放路径
    # 2. 自定义文件 meta 数据
    res = coll_view.load_and_split_text(local_file_path=local_file_path,
                                        metadata={'author': author})
    res = coll_view.load_and_split_text(local_file_path=local_file_path)

    return res


def search_by_vector(db, collection_name):
    # Python SDK 提供了 search() 按照 Vector 搜索的能力，可根据指定的多个向量查找 TopK 个相似性结果。
    # 如下示例，检索与 vectors 字段指定的三组向量数据分别相似，且满足 bookName 条件表达式的 Top3 数据。
    # 1. vectors 指定了需检索的向量数据。
    # 2. filter 指定了 bookName 字段的条件表达式，过滤数据。
    # 3. limit 限制每个单元返回的相似性数据的条数，如 vector 写入三组向量数据，limit 为3，则每组向量返回 top3 的相似数据。
    # 4. params 指定索引类型对应的查询参数，HNSW 类型需要设置 ef，指定查询的遍历范围。
    coll = db.collection(collection_name)
    doc_lists = coll.search(
        vectors=[[0.3123, 0.43, 0.213], [0.315, 0.4, 0.216], [0.40, 0.38, 0.26]],
        filter=Filter(Filter.In("bookName", ["三国演义", "西游记"])),
        params=SearchParams(ef=200),
        limit=3
    )

    """
    说明：
    1、输出结果的顺序，与搜索时设置的 vectors 配置的向量值的顺序一致。如下示例，0下面的三行结果对应[0.3123, 0.43, 0.213]向量的相似度查询结果。1下面的三行结果对应[0.315, 0.4, 0.216]的查询结果。
    2、每一个查询结果都返回 TopK 条相似度计算的结果。其中，K为 limit 设置的数值，如果插入的数据不足 K 条，则返回实际检索到的 Document 数量。
    3、检索结果会按照与查询向量的相似程度进行排列，相似度最高的结果会排在最前面，相似度最低的结果则排在最后面。相似程度则通过 L2（欧几里得距离）、IP（内积）或 COSINE（余弦相似度）计算得出的分数来衡量，输出参数 score 表示相似性计算分数。其中，欧式距离（L2）计算所得的分数越小与搜索值越相似；而余弦相似度（COSINE）与 内积（IP） 计算所得的分数越大与搜索值越相似。
    """
    for i, docs in enumerate(doc_lists):
        print(i)
        for doc in docs:
            print(doc)

    return doc_lists


def search_by_id(db, collection_name):
    """
    # 基于 Doc ID 相似度检索
    # document_ids 指定了检索文档 id【如bookName】
    # filter 指定了过滤条件
    # params 指定索引类型对应的查询参数，HNSW 类型需要设置 ef，指定查询的遍历范围;IVF 系列需要设置 nprobe,指定查询的单位数量
    # retrieve_vector 指定是否输出向量字段
    # limit 指定返回最相似的 Top K 条结果。如果插入的数据不足 K 条，则返回实际插入的 Document 数量。
    # output_fields 指定输出字段

    :param db:
    :return:
    """
    coll = db.collection(collection_name)
    doc_lists = coll.searchById(
        document_ids=['0001', '0002'],
        filter=Filter(Filter.In("bookName", ["三国演义", "西游记"])),
        params=SearchParams(ef=200),
        limit=3
    )

    """
    说明：
    输出的 Document ID 顺序与查询时配置的参数 document_ids 输入的顺序一致。查询结果中0下面的三行为 id 为0001进行相似度查询的结果，1下面的三行为 id 为0002进行相似度查询的结果。
    """
    for i, docs in enumerate(doc_lists):
        print(i)
        for doc in docs:
            print(doc)


def search_by_text(db, collection_name):
    """
    支持检索与输入的文本信息相似的文本
    说明：
        params：指定索引类型对应的查询参数。其中，ef 为 HWSN 索引类型对应的检索参数，指定寻找节点邻居遍历的范围，默认为200。ef 越大，召回率越高。
        filter：指定了 bookName 字段的条件表达式，过滤数据。
        limit： 限制每个单元返回的相似性数据的条数，如 limit 为3，则返回 top3 的相似数据。
        retrieve_vector 指定是否输出向量字段。示例中，文本信息被 Embedding 向量化为768 维数据，数据量大，不变展示，设置为 False。
        output_fields：可自定义需要输出的字段。若不自定，则返回所有字段。

    :return:
    """
    coll = db.collection(collection_name)
    doc_lists = coll.searchByText(
        embeddingItems=['天下大势，分久必合，合久必分'],
        filter=Filter(Filter.In("bookName", ["三国演义", "西游记"])),
        params=SearchParams(ef=200),
        limit=3,
        retrieve_vector=False,
        output_fields=['bookName', 'author', 'text']
    )

    """
    说明：
    检索结果将按照相似程度的高低排列。相似度最高的结果会排在最前面，最低的结果则排在后面。
    相似程度则通过 L2（欧几里得距离）、IP（内积）或 COSINE（余弦相似度）计算得出的分数来衡量。
    输出参数 score 表示相似性计算分数。其中，欧式距离（L2）计算所得的分数越小与搜索值越相似；
    而余弦相似度（COSINE）与 内积（IP） 计算所得的分数越大与搜索值越相似。
    """
    for i, docs in enumerate(doc_lists.get("documents")):
        print(i)
        for doc in docs:
            print(doc)


def get_document_set(db, collection_name, document_set_name):
    """
    上传文件可能存在延迟，查询文件，以便确认文件已在后台解析完成。如下示例，指定文件名，查询存储于数据库中的文件状态。返回参数 indexedStatus 将显示文件预处理、Embedding 向量化的状态。
    New：等待解析。
    Loading：文件解析中。
    Failure：文件解析、写入出错。
    Ready：文件解析、写入完成。

    :param document_set_name:
    :param db:
    :param collection_name:
    :return:
    """
    coll_view = db.collection(collection_name)
    res = coll_view.get_document_set(document_set_name=document_set_name)

    print(vars(res))

    return res


def search_by_file(db, collection_name, document_set_name, content):
    """
    确认文件已解析完成之后，便可开始进行相似性内容检索。如下示例，检索信息什么是向量数据库，默认返回相似度最高的信息。
    :param content:
    :param db:
    :param collection_name:
    :param document_set_name:
    :return:
    """
    coll_view = db.describe_collection_view(collection_view_name=collection_name)

    # 第一步，判断文件上传状态
    # 获取文档集

    ds = coll_view.get_document_set(document_set_name=document_set_name)
    # 获取 indexedStatus 的值
    indexed_status = ds.indexed_status
    # 判断 indexed_status 如果等于 Ready
    if indexed_status == 'Ready':
        # 第二步：确认文件已解析完成之后，便可开始进行相似性内容检索。如下示例，检索信息什么是向量数据库，默认返回相似度最高的信息。
        # content 指定需检索的文本内容
        # document_set_name 指定检索的文件名
        doc_list = coll_view.search(
            content=content,
            document_set_name=[document_set_name]
        )

        # for doc in doc_list:
        #     print(vars(doc))
    else:
        raise Exception("文件未上传完成，请稍后再试")

    return doc_list


if __name__ == '__main__':
    db = get_db("vector-test")
    doc_list = search_by_file(db, "embedding-test", "商城规则.md", "结算单查询规则")
    for doc in doc_list:
        print(vars(doc))