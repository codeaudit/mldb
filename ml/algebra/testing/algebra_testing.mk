# This file is part of MLDB. Copyright 2015 Datacratic. All rights reserved.

$(eval $(call test,least_squares_test,algebra utils arch,boost))
$(eval $(call test,remove_dependent_test,algebra,boost))
