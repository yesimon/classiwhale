/*
 * types.h
 *
 *  Created on: Jul 17, 2010
 *      Author: dan
 */

#ifndef TYPES_H_
#define TYPES_H_

#include <boost/dynamic_bitset.hpp>
#include <string>
#include <vector>

namespace lsd {

struct TweetDigest
{
  long id;
  std::vector<std::string> tokens;
  long author;
  long post_date;
  long rate_date;
  bool rating;
};

struct TweedUser
{
  long id;
  boost::dynamic_bitset<> prefs;
  boost::dynamic_bitset<> rated;
};

}


#endif /* TYPES_H_ */
