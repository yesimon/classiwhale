/*
 * parser.h
 *
 *  Created on: Jul 17, 2010
 *      Author: dan
 */

#ifndef PARSER_H_
#define PARSER_H_

#include "types.h"

#include <string>

namespace lsd {
  TweetDigest digest_tweet (long          tweet_id,
                            std::string   tweet_text,
                            long          author,
                            long          post_date,
                            long          rate_date,
                            bool          rating);
}

#endif /* PARSER_H_ */
