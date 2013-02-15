# Commented out because this test is so slow to run in routine work.

# from __future__ import division
#
# from operator import gt, mul
# import itertools
# import random
# from statlib import stats
# from collections import Counter
#
# from django.test import TestCase
# from django.contrib.auth.models import User
#
# from signalbox.allocation import allocate
# from signalbox.models import Study, Membership
#
# from signalbox.tests.helpers import make_user
#
#
#
# class Test_Allocation(TestCase):
#     """Various tests of randomising Memberships to StudyConditions."""
#
#     fixtures = ['minimal.json',]
#
#     def simulate_recruitment(self, study, user, N=100):
#         """Take a study and user. Allocate N users -> Return allocations counts"""
#
#         mems = [Membership(study=study, user=user) for i in range(1,N)]
#         _ = [allocate(i) for i in mems]
#         initial = range(1,study.studycondition_set.all().count()+1)
#         allocations = Counter([i.condition.id for i in mems]+initial)
#         allocations = allocations - Counter(initial)
#         return allocations
#
#
#     def test_allocation(self):
#         """Simulate studies and check we have sane allocation ratios at N=30."""
#
#         study = Study.objects.get(slug='TESTSTUDY')
#         user = make_user({'username': "TEST", 'email':"TEST@TEST.COM", 'password': "TEST"})
#
#
#         # note - we just test this, because it uses weighted_ranomisation too
#         study.allocation_method = "balanced_groups_adaptive_randomisation"
#
#         # this is the default value anyway
#         study.randomisation_probability = .5
#         study.save()
#
#         one, two, three = study.studycondition_set.all()
#         REPS = 50
#
#         # repeat the test with different group weightings
#         testgroupweights = [ [1,1,1], [1,1,3], ] # [1,2,3], [1,1,6] ]
#         for w1, w2, w3 in testgroupweights:
#             [i.delete() for i in study.membership_set.all()]
#             SAMPLESIZE = 30
#             one.weight = w1
#             two.weight = w2
#             three.weight = w3
#             one.save()
#             two.save()
#             three.save()
#             weights = [i.weight for i in study.studycondition_set.all().order_by('pk')]
#             totalweight = sum(weights)
#             normalisedweights = [float(i)/totalweight for i in weights]
#             expected_counts = [int(SAMPLESIZE*i) for i in normalisedweights]
#
#             random.seed(1234)
#             counters = [self.simulate_recruitment(study, user, N=SAMPLESIZE).items() for j in range(REPS)]
#             observed = zip(* [[i[1] for i in j] for j in zip(*counters)] )
#
#             maxgroupimbalance = max([ max(abs(i-j) for i,j in zip(k, expected_counts) ) for k in observed])
#             maxtotalimbalance = max([ sum(abs(i-j) for i,j in zip(k, expected_counts) ) for k in observed])
#             minpval = min([stats.chisquare( i, f_exp=expected_counts )[1] for i in observed])
#
#             print "maxgroupimbalance, maxtotalimbalance, minpval"
#             print maxgroupimbalance, maxtotalimbalance, minpval
#
#             # this is a stupid test, but it's the best I can think of for the moment
#             # given we set the seed above, it's a loose way of checking we haven't broken things
#             assert minpval > 0.1
#
#
#
#
#
#
