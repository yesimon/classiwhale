//============================================================================
// Name        : lsd.cpp
// Author      : yuzeh
// Version     :
// Copyright   : Copyright 2010 yuzeh
// Description : Hello World in C++, Ansi-style
//============================================================================

#include "parser.h"
#include "types.h"

#include <stdio.h>

int main()
{
  lsd::TweetDigest digest = lsd::digest_tweet(1001,
                                              "http:://www.google.com www.gmail.com @dog #cat subleases on craigslist",
                                              1002,
                                              1003,
                                              1004,
                                              true);

  printf("tweet id: %ld\n", digest.id);
  printf("tweet tokens:\n");

  for (std::vector<std::string>::iterator itr = digest.tokens.begin();
       itr != digest.tokens.end();
       ++itr)
    printf("\t%s\n", (*itr).c_str());

  printf("tweet tokens: %ld\n", digest.id);
  printf("tweet post date: %ld\n", digest.post_date);
  printf("tweet rate date: %ld\n", digest.rate_date);
  printf("tweet rating: %d\n", digest.rating);

  return 0;
}
