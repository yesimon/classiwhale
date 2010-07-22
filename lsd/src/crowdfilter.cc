/*
 * crowdfilter.cc
 *
 *  Created on: Jul 21, 2010
 *      Author: dan
 */

#include "crowdfilter.h"

#include "types.h"

#include <boost/dynamic_bitset.hpp>
#include <vector>

namespace lsd {

static const double LIKES_WEIGHT = 1;
static const double DISLIKES_WEIGHT = 1;

/**
 * Computes these numbers:
 *  - al = how many they both like divided by how many they both rated
 *  - ad = how many they both dislike divided by how many they both rated
 * and returns a weighted sum of both numbers. Guaranteed to be between 0 and 1
 */
double compute_closeness (TweedUser &user1, TweedUser &user2)
{
  boost::dynamic_bitset<> both_rated = (user1.rated & user2.rated);
  int num_like = (user1.prefs & user2.prefs & both_rated).count();
  int num_dislike = ((~(user1.prefs)) & (~(user2.prefs)) & both_rated).count();

  return ((double) num_like) / both_rated.count()
      + ((double) num_dislike) / both_rated.count();
}

}
