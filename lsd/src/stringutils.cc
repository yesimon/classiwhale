/*
 * stringutils.cc
 *
 *  Created on: Jul 18, 2010
 *      Author: dan
 */

#include "stringutils.h"

#include <boost/regex.hpp>
#include <string>

namespace lsd {

/** Determines whether a given token is a hashtag. */
bool is_hashtag (std::string token) { return token[0] == '#'; }

/** Determines whether a given token is referencing a user. */
bool is_referencing_user (std::string token) { return token[0] == '@'; }

/** Determines whether a given token is a url. */
bool is_url (std::string token)
{
  // A token is a url if it matches this regex:
  //    "(https?://)|(www\\.)([-\\w\\d\\.]+)+(:\\d+)?(/([\\w\\d/_\\.]*(\\?\\S+)?)?)?"

  boost::regex e("(https?://)|(www\\.)([-\\w\\.]+)+(:\\d+)?(/([\\w/_\\.]*(\\?\\S+)?)?)?");

  return boost::regex_match(token, e);
}

}
