/*
 * stringutils.h
 *
 * Utilities for parsing tokens in tweets.
 *  Created on: Jul 18, 2010
 *      Author: dan
 */

#ifndef STRINGUTILS_H_
#define STRINGUTILS_H_

#include <boost/regex.hpp>
#include <string>

namespace lsd {

/** Determines whether a given token is a hashtag. */
bool is_hashtag (std::string token);

/** Determines whether a given token is referencing a user. */
bool is_referencing_user (std::string token);

/** Determines whether a given token is a url. */
bool is_url (std::string token);

}

#endif /* STRINGUTILS_H_ */
