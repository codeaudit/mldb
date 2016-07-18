#
# MLDB-1774_test_column_order_by.py
# jonathan, 2016-07-05
# This file is part of MLDB. Copyright 2016 Datacratic. All rights reserved.
#

import unittest
import json

mldb = mldb_wrapper.wrap(mldb)  # noqa



class MLDB1774TestColumnOrderBy(MldbUnitTest):  # noqa

	@classmethod
	def setUpClass(cls):

		mldb.put('/v1/procedures/import_ML_concepts', {
		    "type":"import.text",
		    "params": 
		    {
		        "dataFileUrl":"http://public.mldb.ai/datasets/MachineLearningConcepts.csv",
		        "outputDataset":{
		            "id":"ml_concepts",
		            "type": "sparse.mutable"
		        },
		        "named": "Concepts",
		        "select": 
		            """
		                tokenize(
		                    lower(Text), 
		                    {splitchars: ' -''"?!;:/[]*,().',  
		                    min_token_length: 4}) AS *
		            """,
		        "runOnCreation": True
		    }
		})


	# testing different ways to order columns using COLUMN ordering operations

	def test_column_expr_order_rowCount(self):
		dt1 = mldb.query("""
			SELECT COLUMN EXPR (AS columnName() ORDER BY rowCount() DESC)
			FROM ml_concepts
		""")
		col_list1 = dt1[::1][0]
		expected = ['with', 'learning', 'machine', 'neural', 'model']

		#mldb.log(col_list1[1:6])
		self.assertEqual(cmp(col_list1[1:6], expected), 0);
	

	def test_order_by_vertical_rowCount(self):
		dt2 = mldb.query("""
			SELECT * from (SELECT vertical_count({*}) as * NAMED 'num' FROM ml_concepts)
			ORDER BY num DESC
		""")

		col_list2 = dt2[::1][0]
		expected = ['with', 'learning', 'machine', 'neural', 'model']

		#mldb.log(col_list2[1:6])
		self.assertEqual(cmp(col_list2[1:6], expected), 0);



if __name__ == '__main__':
	mldb.run_tests()
