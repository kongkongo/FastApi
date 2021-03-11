# 做法，主要是提供训练数据。
# 1. 可以先拿真数据。
# 2. 可以再拿不确定数据获取数据。
# 入口参数，总共要多少条数据。
# 真数据多少条，不确定数据多少条。 百分比是多少？
# 下面做的事情是：可以按照分类拿数据，默认的是按照比例获取数据。
# 策略，最大真实数据，百分比数据。

import sys
import pathlib
_project_root = str(pathlib.Path(__file__).resolve().parents[1])
sys.path.append(_project_root)
from server import database 
from basic import schemas
import random
from sqlalchemy.sql import insert
from learning import rule
from sqlalchemy import desc

def get_train_data(max_data_nums=5000, data_percent={"is":0.3,"uncertain":0.7} ,category_percent={}):
    """
    [summary]

    Args:
        max_data_nums ([type]): [ 要获取的训练数据 ]
        data_percent (dict, optional): [数据组成比例，确定数据的组成和不确定数据的组成的比例]. Defaults to {}.
        类别： max，0.3 的结果
        category_percent (dict, optional): [description]. Defaults to {}. 获取训练数据中，各个类别的组成。
    TODO:
    这个应该使用什么设计模式呢？
    做好一些策略，当数据不足的时候怎么办，返回哪些数据？
    返回的结果要定义好。
    关键是参数会影响反馈的结果。
    """
    x_is_data_oid_list=[]
    x_uncertain_oid_list=[]
    # 找到所有数据的ID。
    x_is_data_nums= int(max_data_nums*data_percent["is"])
    x_uncertain_nums= int(max_data_nums*data_percent["uncertain"])
    with database.db_session() as db: 
        x_is_data_oid_list=get_random_data_id_list(x_is_data_nums,database.XIsCategoryTable,db)
        x_uncertain_oid_list=get_random_data_id_list(max_data_nums-len(x_is_data_oid_list),database.XUncertainCategoryTable,db,filer_info={database.XUncertainCategoryTable.finished:0}) # 排除掉哪些已经校验过的数据。
    return_training_data=[]
    for row_data in x_is_data_oid_list+x_uncertain_oid_list:
        if  not row_data[0] :
            print(row_data) 
            continue
        return_training_data.append(
           ( 
               get_vec_by_data_oid(row_data[0]),row_data[1]
           )
        )
    return return_training_data
    # 根据数据的比例获得数据。
    # 之后再去思考如何去掉哪些不要的数据，做一个视图吧。

def get_vec_by_data_oid(data_oid):
    str_vec=""
    list_vec=[]
    with database.db_session() as db:
        str_vec=db.query(database.TextVecTable.vec).filter(database.TextVecTable.data_oid==data_oid).one()
        list_vec=list(map(lambda x:float(x),str_vec.vec.split(',')))
    #print(list_vec)
    return list_vec


def get_random_data_id_list(max_nums,datatable_name,db_conn,filer_info={}):
    """
    [
        根据条件返回指定数量的data_oid 列表。
    ]

    Args:
        max_nums ([type]): [ 返回数据的最大条数]
        datatable_name ([type]): [查询表的ORM定义类]
        db_conn ([type]): [数据库的链接]
        filer_info (dict, optional): [description]. Defaults to {}.

    Returns:
        [type]: [description]
    """    
    query_obj=db_conn.query(datatable_name.data_oid,datatable_name.category)
    for  key,value in filer_info.items():
        query_obj=query_obj.filter(key==value)
    query_data_oid_list=query_obj.all()
    #data_oid_list=[ele[0] for ele in query_data_oid_list]
    random.shuffle(query_data_oid_list)
    return query_data_oid_list[:max_nums]


def get_category_mapping_info():
    with database.db_session() as db:
        info_list=db.query(database.BatchCategoryInfoTable.category,database.BatchCategoryInfoTable.category_id)
        mapping_info={}
        for category,category_id in  info_list:
            mapping_info[category]=category_id
            mapping_info[category_id]=category

    return mapping_info


def get_sure_data(max_num:int ):
    """[summary]

    Args:
        max_num (int): [最大的数据条目]
    获得真的正确的数据，用来做校验。
    直接返回所有的校验的数据就可以了。
    """
    pass 

def get_need_predict_data():
    """
    获得需要验证的数据。
    还有获得原始数据。
    """
    ans_data=[]
    with database.db_session() as db:
        data_list=db.query(database.TextVecTable.data_oid,database.TextVecTable.vec).all()
        for row in data_list:
            list_vec=[ float(x) for x in row.vec.split(',')] #list(map(lambda x:float(x),str_vec.vec.split(',')))
        
            ans_data.append([row.data_oid,list_vec])
    return ans_data
    
def get_need_predict_text_data(): #这里为何返回了 表中的所有txt内容
    """
    [返回文本数据,主要为规则提供数据接口]
    TODO: 一次拿到所有的文本内容，在数据量大的时候可能会出现问题。需要优化后期

    Returns:
        [type]: [description]
    """
    ans_data = []
    with database.db_session() as db:
        data_list = db.query(database.OriginTextDataTable.data_oid,database.OriginTextDataTable.text).all() #是否该添加限制条件，来做一个查询数量的限制。
        for row in data_list:
            yield [row.data_oid, row.text]


import json
import numpy as np
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def update_predict_data(meta_info,batch_id=0,ai_id=0):
    """[summary]

    Args:
        data_id ([int]): [description]
        meta_info ([dict]): 
                {
                    "category_id": 2,
                    "decision_list": [
                        0.849419160098665,
                        3.2599307808093747,
                        2.118750077455952,
                        -0.25528040257805545
                    ],
                    "proba_list": [
                        0.0013409690326336684,
                        0.9808453085781627,
                        0.01730583467187295,
                        0.0005078877173305729
                    ],
                    "category": "预计的业绩",
                    "data_oid": 7
                }
        
        batch_id (int, optional): [description]. Defaults to 0.
        ai_id (int, optional): [description]. Defaults to 0.

    Returns:
        [type]: [description]
    """    
    data_oid=meta_info["data_oid"]
    for db in database.get_db():
        query_result_list=db.query(database.AiPredictonOfResultsTable).filter(database.AiPredictonOfResultsTable.batch_id==batch_id).filter(database.AiPredictonOfResultsTable.ai_id==ai_id).filter(database.AiPredictonOfResultsTable.data_oid==data_oid)
        str_meta_info=json.dumps(meta_info,ensure_ascii=False,indent=4,cls=NpEncoder)
        if query_result_list.count() >0:
            ai_predict_ret_obj=query_result_list.one()
            ai_predict_ret_obj.meta_info
            db_meta_info=json.loads(ai_predict_ret_obj.meta_info)
            #print(db_meta_info)
            if meta_info["category"]!= db_meta_info["category"] :
                ai_predict_ret_obj.category=meta_info["category"]
                ai_predict_ret_obj.meta_info=str_meta_info
                db.commit() # update data in database
        else:

            ai_ret_obj=database.AiPredictonOfResultsTable(
                data_oid=data_oid,
                category=meta_info["category"],
                batch_id=batch_id,
                ai_id=ai_id,
                meta_info=str_meta_info
                )
            db.add(ai_ret_obj)
            db.commit()
        return 0
    return 1
    #print(list_vec)


    pass

def update_predict_data_rule(meta_info,batch_id=0,model_id=0):
    # 更新一下数据
    """
    [

    ]
    Args:
        meta_info ([dict]): meta_info ([dict]): 
                {
                    "category_id": 2,
                    "category": "预计的业绩",
                    "data_oid": 7
                }
        
        batch_id (int, optional): [description]. Defaults to 0.
        ai_id (int, optional): [description]. Defaults to 0.
    """
    data_oid=meta_info["data_oid"]
    for db in database.get_db():
        query_result_list=db.query(database.RulePredictionOfResultsTable).filter(database.RulePredictionOfResultsTable.batch_id==batch_id).filter(database.RulePredictionOfResultsTable.model_id==model_id).filter(database.RulePredictionOfResultsTable.data_oid==data_oid)
        str_meta_info=json.dumps(meta_info,ensure_ascii=False,indent=4,cls=NpEncoder)
        if query_result_list.count() >0:
            rule_predict_ret_obj=query_result_list.one()
            db_meta_info=json.loads(rule_predict_ret_obj.meta_info)
            print(db_meta_info)
            if meta_info["category"]!= rule_predict_ret_obj.category :
                rule_predict_ret_obj.category=meta_info["category"]
                rule_predict_ret_obj.meta_info=str_meta_info
                db.commit() # update data in database
        else:
            rule_predict_ret_obj=database.RulePredictionOfResultsTable(
                data_oid=data_oid,
                category=meta_info["category"],
                batch_id=batch_id,
                model_id=model_id,
                meta_info=str_meta_info
                )
            db.add(rule_predict_ret_obj)
        db.commit()
# ref http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters

def update_metric_info(meta_info,hai_type,batch_id=0,hai_id=0):
    """
    [
        更新metric的数据
    ]

    Args:
        meta_info ([type]): [description]
        hai_type ([type]): [description]
        batch_id (int, optional): [description]. Defaults to 0.
        hai_id (int, optional): [description]. Defaults to 0.
    """
    with database.db_session() as db:
        query_result_list = db.query(database.MetricInfoTable).filter(database.MetricInfoTable.hai_type==hai_type).filter(database.MetricInfoTable.batch_id==batch_id).filter(database.MetricInfoTable.hai_id==hai_id)
        str_meta_info = json.dumps(meta_info,ensure_ascii=False,indent=4,cls=NpEncoder)
        if query_result_list.count() > 0:
            metric_info_obj = query_result_list.one()
            metric_info_obj.meta_info = str_meta_info
        else:
            metric_info_obj = database.MetricInfoTable(
                batch_id=batch_id,
                hai_id=hai_id,
                hai_type=hai_type,
                meta_info=str_meta_info
                )
            db.add(metric_info_obj)
        db.commit()

def update_uncentain_data(meta_info,batch_id=0):
    """
    [
        summary
    ]

    Args:
        meta_info ([type]): [description]
        batch_id (int, optional): [description]. Defaults to 0.
    """
    data_oid=meta_info["data_oid"]
    # todo 米桂田.
    for db in database.get_db():
        query_result_list=db.query(database.XUncertainCategoryTable).filter(database.XUncertainCategoryTable.data_oid==data_oid).filter(database.XUncertainCategoryTable.batch_id==batch_id)
        if query_result_list.count() >0:
            rule_predict_ret_obj=query_result_list.one()
            rule_predict_ret_obj.category=meta_info["category"]
            rule_predict_ret_obj.category_from=meta_info["category_from"]
            rule_predict_ret_obj.prob=meta_info["prob"]
            rule_predict_ret_obj.finished=0
            rule_predict_ret_obj.judgment_type=0
            rule_predict_ret_obj.judgment_category="null"
        else:
            rule_predict_ret_obj=database.XUncertainCategoryTable(
                batch_id=batch_id,
                data_oid=data_oid,
                category=meta_info["category"],
                prob=meta_info["prob"],
                category_from=meta_info["category_from"]
                )
            db.add(rule_predict_ret_obj)
        db.commit()

    pass

def get_ai_prediction_result(batch_id=0,ai_id=0):
    """[summary]

    Args:
        batch_id (int, optional): [批量号码]. Defaults to 0.
        ai_id (int, optional): [模型预测密码]. Defaults to 0.

    Returns:
        List[database.AiPredictonOfResultsTable]: [
            [{
        "data_id":1,
        "category":"",
        "proba":0.2,
            }]

        ]
    """
    ans_data={}
    # ans_data={
    #     "data_oid":{},
    # }
    for db in database.get_db():
        data_list=db.query(database.AiPredictonOfResultsTable.data_oid,database.AiPredictonOfResultsTable.meta_info,database.AiPredictonOfResultsTable.category).filter(database.AiPredictonOfResultsTable.batch_id==batch_id).filter(database.AiPredictonOfResultsTable.ai_id==ai_id)
        metric_info=get_metric_info(ai_id,"ai_{}".format(ai_id)) 
        for data in data_list:
            data_info_dict=json.loads(data.meta_info)
            proba=0.1
            
            try:
                data_info_dict=json.loads(data.meta_info)
                category_id=data_info_dict["category_id"]
                # 这一步用来计算可能,数据可能是这一类真正的概率.
                # 
                category=data_info_dict["category"]
                current_proba=data_info_dict["proba_list"][category_id-1]# 获取概率
                precision=metric_info["precision"].get(category,1)
                proba=current_proba*precision
                
            except Exception as identifier:
                print(identifier)

            ans_data[data.data_oid]={
                "data_oid":data.data_oid,
                "category":data.category ,
                "category_id":category_id,
                "proba": proba
                }

    return ans_data

    # return [{
    #     "data_id":1,
    #     "category":"",
    #     "proba":0.2,
    # }]

def get_rule_prediction_result(batch_id=0,model_id=0):
    """
    [
        获取规则系统预测的数据结果,返回的是一个字典
    ]

    Args:
        batch_id (int, optional): [批量号码]. Defaults to 0.
        ai_id (int, optional): [模型预测号码]. Defaults to 0.

    Returns:
        List[database.AiPredictonOfResultsTable]: [
            [{
        "data_id":1,
        "category":"",
        "proba":0.2,
            }]

        ]
    """
    ans_data={}
    with database.db_session() as db:
        data_list=db.query(database.RulePredictionOfResultsTable.data_oid,database.RulePredictionOfResultsTable.meta_info,database.RulePredictionOfResultsTable.category).filter(database.RulePredictionOfResultsTable.batch_id==batch_id).filter(database.RulePredictionOfResultsTable.model_id==model_id)
        metric_info=get_metric_info(model_id,"hi_{}".format(model_id)) 
        for data in data_list:
            data_info_dict=json.loads(data.meta_info)
            proba=0.01 # 这里面应该有一个计算过程的可以计算出来真正的概率,具体的逻辑我还有想出来,想到了就从一个地方去计算吧,这个是可以计算出来的.
            try:
                data_info_dict=json.loads(data.meta_info)
                category_id=data_info_dict["category_id"]
                category=data_info_dict["category"]
                precision=metric_info["precision"].get(category,proba) # 注意这部分计算概率的方式和ai的计算方式不一样,以后还是需要改善的,其实使用贝叶斯的算法可能更好一点.
                proba=precision
            except Exception as identifier:
                print(identifier)

            ans_data[data.data_oid]={
                "data_oid":data.data_oid,
                "category":data.category ,
                "category_id":category_id,
                "proba": proba
                }
    return ans_data

def get_rule_model_group(batch_id: str) -> dict:
    """
    根据batch_id,获得此批次的规则模型组，供加载使用

    Args:
        batch_id (int): 批次ID
    
    Returns:
        {category：{rule_model}}
    """
    if not isinstance(batch_id, str):
        batch_id = str(batch_id)
    rule_model_group = {}
    category_list = []
    for db in database.get_db():
        query_categry_list = db.query(database.BatchRegularInfoTable.category_id).filter(database.BatchRegularInfoTable.batch_id == batch_id).group_by(database.BatchRegularInfoTable.category_id)
        if query_categry_list.count() == 0:
            return rule_model_group   #TODO: 返回是空如何处理
        else:
            for query_categry in query_categry_list:
                category_list.append(query_categry[0])
        for category_id in category_list:
            pos_patterns_list = []
            neg_patterns_list = []
            query_result_list = db.query(database.BatchRegularInfoTable).filter(database.BatchRegularInfoTable.batch_id == batch_id, database.BatchRegularInfoTable.category_id == category_id)
            for query_result in query_result_list:
                if query_result.regular_type == 'pos':
                        pos_patterns_list.append(query_result.content)
                elif query_result.regular_type == 'neg':
                    neg_patterns_list.append(query_result.content)
                else:
                    pass  #TODO: 是否还会有其他类型的规则，是否需要处理
            category = db.query(database.BatchCategoryInfoTable.category).filter(database.BatchCategoryInfoTable.category_id == category_id).one()
            rule_model_group[category[0]] = {
                    "origin_pos_patterns": pos_patterns_list,
                    "origin_neg_patterns": neg_patterns_list
                }
    return rule_model_group

def get_metric_info(hai_id,hai_type,batch_id=0):
    """
    Args:
        hai_id ([type]): [description]
        hai_type ([type]): [description]
        batch_id (int, optional): [description]. Defaults to 0.

    Returns:
        dict: [
            example:
                {
                    "precision": {
                        "业绩预告期间": 1.0,
                        "UNKNOW": 0.5526315789473685,
                        "预计的业绩": 0.9259259259259259,
                        "元信息": 0.0
                    },
                    "recall": {
                        "业绩预告期间": 0.89375,
                        "UNKNOW": 0.9545454545454546,
                        "预计的业绩": 0.9615384615384616,
                        "元信息": 0.0
                    },
                    "F-measure": {
                        "业绩预告期间": 0.9438943894389439,
                        "UNKNOW": 0.7000000000000001,
                        "预计的业绩": 0.9433962264150944,
                        "元信息": 0.0
                    },
                    "support_info": {
                        "业绩预告期间": 160,
                        "UNKNOW": 22,
                        "预计的业绩": 26,
                        "元信息": 1
                    }
                }
        ]
    """    
 
    ans_data={}
    with database.db_session() as db:
        query_data_list=db.query(database.MetricInfoTable.meta_info).filter(database.MetricInfoTable.batch_id==batch_id).filter(database.MetricInfoTable.hai_id==hai_id).filter(database.MetricInfoTable.hai_type==hai_type)
        if query_data_list.count()>0:
            data=query_data_list.one()
            metric_info=json.loads(data.meta_info)
            return metric_info
        else:
            return  {
                    "precision": {
                        # "业绩预告期间": 1.0,
                        # "UNKNOW": 0.5526315789473685,
                        # "预计的业绩": 0.9259259259259259,
                        # "元信息": 0.0
                    },
                    "recall": {
                        # "业绩预告期间": 0.89375,
                        # "UNKNOW": 0.9545454545454546,
                        # "预计的业绩": 0.9615384615384616,
                        # "元信息": 0.0
                    },
                    "F-measure": {
                        # "业绩预告期间": 0.9438943894389439,
                        # "UNKNOW": 0.7000000000000001,
                        # "预计的业绩": 0.9433962264150944,
                        # "元信息": 0.0
                    },
                    "support_info": {
                        # "业绩预告期间": 160,
                        # "UNKNOW": 22,
                        # "预计的业绩": 26,
                        # "元信息": 1
                    }
                }




def get_x_is_category_data():
    """
    [
        从x_is_category和 XUncertainCategoryTable 中获取预测的数据,
        方便计算预测数据的准确率,
    ]

    Returns:
        list: [ {data_oid:"",category:""} ]
    """    
    ans_data_info={}
    with database.db_session() as db:
        # 从XIsCategoryTable和XUncertainCategoryTable 中取出数据出来,可以知道数据的真实值和预测值
        data_list=db.query(database.XIsCategoryTable.data_oid,database.XIsCategoryTable.category)
        for data in data_list:
            ans_data_info[data.data_oid]={
                    "data_oid":data.data_oid,"category":data.category
                }
            
    return ans_data_info

def get_x_is_not_category_data():
    """
    [
        从 XISNOTCategory 的数据,方便计算预测数据的准确数值.
    ]

    Returns:
        list: [{data_oid:"",category:""}]
    """

    # 从XISNOTCategory中取出数据出来 和 XUncertainCategoryTable 中 取出数据出来,用来进一步了解预测的精确率,情况.
    # 前提条件是: 
    # 1. XISNOTCategory 中的dataoid,不在XIsCategoryTable 中出现.
    # 2. XISNOTCategory data_oid对应的category和XUncertainCategoryTable 的值是一样的.
    ans_data_info={}
    with database.db_session() as db:
        # 从XIsCategoryTable和XUncertainCategoryTable 中取出数据出来,可以知道数据的真实值和预测值
        #https://blog.csdn.net/weixin_42752248/article/details/106079115 order by
        data_list=db.query(database.XUncertainCategoryTable.data_oid,database.XUncertainCategoryTable.category).order_by(database.XUncertainCategoryTable.data_oid)
        for data in data_list:
            ans_data_info[data.data_oid]={
                    "data_oid":data.data_oid,"category":data.category
                }
            
    return ans_data_info

if __name__ == "__main__":
    #return_training_data=get_train_data(20000)
    #print(return_training_data)
    #get_vec_by_data_oid(3540)
    mapping_info=get_category_mapping_info()
    print(mapping_info)
    #get_need_predict_data()
    meta_info={
                "category_id": 2,
                "decision_list": [
                    0.849419160098665,
                    3.2599307808093747,
                    2.118750077455952,
                    -0.25528040257805545
                ],
                "proba_list": [
                    0.0013409690326336684,
                    0.9808453085781627,
                    0.01730583467187295,
                    0.0005078877173305729
                ],
                "category": "UNKNOW",
                "data_oid": 7
            }
    #update_predict_data(meta_info=meta_info,)
    get_rule_prediction_result()
    #get_need_predict_text_data()
    get_ai_prediction_result()
    #get_rule_prediction_result()
    get_x_is_category_data()
    get_x_is_not_category_data()
    get_metric_info(0,"ai_0")