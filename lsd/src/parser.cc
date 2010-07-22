/*
 * parser.cpp
 *
 *  Created on: Jul 17, 2010
 *      Author: dan
 */

#include "parser.h"

#include "stringutils.h"
#include "types.h"

#include <boost/tokenizer.hpp>
#include <string>
#include <vector>

namespace lsd {

std::vector<std::string> parse_tweet_text (std::string tweet_text);

TweetDigest digest_tweet (long          tweet_id,
                          std::string   tweet_text,
                          long          author,
                          long          post_date,
                          long          rate_date,
                          bool          rating)
{
  TweetDigest ret;
  ret.id = tweet_id;
  ret.tokens = parse_tweet_text(tweet_text);
  ret.author = author;
  ret.post_date = post_date;
  ret.rate_date = rate_date;
  ret.rating = rating;

  return ret;
}

std::vector<std::string>
parse_tweet_text (std::string tweet_text)
{
  // TODO: create custom TokenizerFunction to only accept spaces
  boost::tokenizer<> _tokenizer(tweet_text);
  std::vector<std::string> tokens;

  for (boost::tokenizer<>::iterator itr = _tokenizer.begin();
       itr != _tokenizer.end();
       ++itr)
  {
    std::string token = *itr;
    if (is_hashtag(token))
      token = "_ hashtag";
    if (is_referencing_user(token))
      token = "_ userref";
    if (is_url(token))
      token = "_ url";
    tokens.push_back(token);
  }

  return tokens;
}

}
