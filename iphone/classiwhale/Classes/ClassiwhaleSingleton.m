//
//  ClassiwhaleSingleton.m
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import "ClassiwhaleSingleton.h"
#import "SA_OAuthTwitterEngine.h"
#import "classiwhaleAppDelegate.h"
#import "JSON.h"


#define kOAuthConsumerKey				@"H3jdfPuU3srfX2uo7LFQ1w"
#define kOAuthConsumerSecret			@"Fe0iHcfi8nubMBzjbcUuf6zRW8Nn9VgMJkiHcCdKwSw"

@implementation ClassiwhaleSingleton

@synthesize authenticated;
@synthesize cookies;

static ClassiwhaleSingleton *sharedInstance = nil;

// Get the shared instance and create it if necessary.
+ (ClassiwhaleSingleton*)sharedInstance {
	if (sharedInstance == nil) {
		sharedInstance = [[super allocWithZone:NULL] init];
	}
	
	return sharedInstance;
}

- (void) loginToTwitter:(UIViewController*)vc
{
	connections = CFDictionaryCreateMutable(kCFAllocatorDefault, 0,
																					&kCFTypeDictionaryKeyCallBacks, &kCFTypeDictionaryValueCallBacks);
	twitterEngine = [[SA_OAuthTwitterEngine alloc] initOAuthWithDelegate: self];
	twitterEngine.consumerKey = kOAuthConsumerKey;
	twitterEngine.consumerSecret = kOAuthConsumerSecret;
	UIViewController *controller = [SA_OAuthTwitterController controllerToEnterCredentialsWithTwitterEngine: twitterEngine delegate: self];
	
	if (controller) 
		[vc presentModalViewController: controller animated: YES];
	else 
		[twitterEngine sendUpdate: [NSString stringWithFormat: @"Already Updated. %@", [NSDate date]]];	
}

- (NSDictionary *) getTimelineWithResponse:(NSURLResponse **)response andError:(NSError **)error
{
  if(!authenticated) return nil;
  NSMutableURLRequest* request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"http://classiwhale.com/api/twitter/timeline"]];
  [request setHTTPMethod: @"POST"];
  [request setHTTPShouldHandleCookies:NO];
  
  if(cookies != nil) {
    [request setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:self.cookies]];
  }
  
  *response = nil;
  *error = nil;
  
  NSData *dat = [NSURLConnection sendSynchronousRequest:request returningResponse:response error:error];
  NSLog(@"Response = %@", *response);
  NSLog(@"Error = %@", *error);
  if(*error != nil) return nil;
  NSString *json_string = [[NSString alloc] initWithData:dat encoding:NSUTF8StringEncoding];
  NSDictionary *arr = [json_string JSONValue];
  return arr;
}

- (NSDictionary *) getFilteredTimelineWithResponse:(NSURLResponse **)response andError:(NSError **)error
{
  if(!authenticated) return nil;
  NSMutableURLRequest* request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"http://classiwhale.com/api/twitter/filtered"]];
  [request setHTTPMethod: @"POST"];
  [request setHTTPShouldHandleCookies:NO];
  
  if(cookies != nil) {
    [request setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:self.cookies]];
  }
  
  *response = nil;
  *error = nil;
  
  NSData *dat = [NSURLConnection sendSynchronousRequest:request returningResponse:response error:error];
  NSLog(@"Response = %@", *response);
  NSLog(@"Error = %@", *error);
  if(*error != nil) return nil;
  NSString *json_string = [[NSString alloc] initWithData:dat encoding:NSUTF8StringEncoding];
  NSDictionary *arr = [json_string JSONValue];
  return arr;
}

- (NSDictionary *) getSearchWithResponse:(NSURLResponse **)response andError:(NSError **)error andQuery:(NSString *)q
{
  if(!authenticated) return nil;
	NSString* urlString = [NSString stringWithFormat:@"http://classiwhale.com/api/twitter/search?q=%@", q];

  NSMutableURLRequest* request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:urlString]];
  [request setHTTPMethod: @"POST"];
  [request setHTTPShouldHandleCookies:NO];
  
  if(cookies != nil) {
    [request setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:self.cookies]];
  }
  
  *response = nil;
  *error = nil;
  
  NSData *dat = [NSURLConnection sendSynchronousRequest:request returningResponse:response error:error];
  NSLog(@"Response = %@", *response);
  NSLog(@"Error = %@", *error);
  if(*error != nil) return nil;
  NSString *json_string = [[NSString alloc] initWithData:dat encoding:NSUTF8StringEncoding];
  NSDictionary *arr = [json_string JSONValue];
  return arr;
}


- (NSArray *) getFriendsWithResponse:(NSURLResponse **)response andError:(NSError **)error
{
  if(!authenticated) return nil;
  NSMutableURLRequest* request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"http://classiwhale.com/api/twitter/friends"]];
  [request setHTTPMethod: @"POST"];
  [request setHTTPShouldHandleCookies:NO];
  
  if(cookies != nil) {
    [request setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:self.cookies]];
  }
  
  *response = nil;
  *error = nil;
  
  NSData *dat = [NSURLConnection sendSynchronousRequest:request returningResponse:response error:error];
  NSLog(@"Response = %@", *response);
  NSLog(@"Error = %@", *error);
  if(*error != nil) return nil;
  NSString *json_string = [[NSString alloc] initWithData:dat encoding:NSUTF8StringEncoding];
  NSArray *arr = [json_string JSONValue];
  return arr;
}

- (NSArray *) rateTweetId:(NSString *)tweet_id up:(BOOL)rate_up withResponse:(NSURLResponse **)response andError:(NSError **)error
{
  if(!authenticated) return nil;

  NSString *base_string = @"http://classiwhale.com/api/twitter/rate/?id=";
  NSString *id_string = [base_string stringByAppendingString:tweet_id];
  NSString *complete_string = [id_string stringByAppendingString:(rate_up ? @"&rating=up" : @"&rating=down")];
  NSMutableURLRequest* request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:complete_string]];
  [request setHTTPMethod: @"GET"];
  [request setHTTPShouldHandleCookies:NO];
  
  if(cookies != nil) {
    [request setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:self.cookies]];
  }
  
  *response = nil;
  *error = nil;
  
  NSData *dat = [NSURLConnection sendSynchronousRequest:request returningResponse:response error:error];
  NSLog(@"Response = %@", *response);
  NSLog(@"Error = %@", *error);
  if(*error != nil) return nil;
  NSString *json_string = [[NSString alloc] initWithData:dat encoding:NSUTF8StringEncoding];
  NSArray *arr = [json_string JSONValue];
  return arr;
}

- (NSDictionary *) getFriendTimeline:(NSString *)friend_id withResponse:(NSURLResponse **)response andError:(NSError **)error
{
  
  NSString *base_string = @"http://classiwhale.com/api/twitter/friend/timeline/?id=";
  NSString *complete_string = [base_string stringByAppendingString:friend_id];
  NSMutableURLRequest* request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:complete_string]];
  [request setHTTPMethod: @"GET"];
  [request setHTTPShouldHandleCookies:NO];
  
  if(cookies != nil) {
    [request setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:self.cookies]];
  }
  
  *response = nil;
  *error = nil;
  
  NSData *dat = [NSURLConnection sendSynchronousRequest:request returningResponse:response error:error];
  NSLog(@"Response = %@", *response);
  NSLog(@"Error = %@", *error);
  if(*error != nil) return nil;
  NSString *json_string = [[NSString alloc] initWithData:dat encoding:NSUTF8StringEncoding];
  NSDictionary *arr = [json_string JSONValue];
  return arr;
}

- (void) fetchProfilePic:(NSString*) urlString
{
	NSURL* url = [[[NSURL alloc] initWithString:urlString] autorelease];
	[self createConnection:url postBody:nil method:@"GET" cid:urlString];
}

- (void) createConnection:(NSURL*)url postBody:(NSData*)postBody method:(NSString*)method cid:(NSString*)cid
{
	NSMutableURLRequest* request = [[NSMutableURLRequest alloc] initWithURL:url];
	if (postBody) [request setHTTPBody:postBody];
	[request setHTTPMethod:method];
	[request setTimeoutInterval:30.0];
	NSURLConnection *connection=[[NSURLConnection alloc] initWithRequest:request delegate:self];
	if (connection) {		
		CFDictionaryAddValue(connections, connection,
												 [NSMutableDictionary dictionaryWithObjectsAndKeys: @"expires", [NSDate date], cid, @"id", [NSMutableData data], @"receivedData", nil]);
	} else {
    NSLog(@"Connection Failed");
	}
	[request release];
}

//======================================================================================================
//HTTP Request stuff

- (void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data
{
	const NSMutableDictionary *connectionInfo = CFDictionaryGetValue(connections, connection);
	[[connectionInfo objectForKey:@"receivedData"] appendData:data];
}

- (void)connectionDidFinishLoading:(NSURLConnection *)connection
{	
	const NSMutableDictionary *connectionInfo = CFDictionaryGetValue(connections, connection);
	NSData* data = [connectionInfo objectForKey:@"receivedData"];
	NSString *connectionID = [connectionInfo objectForKey:@"id"];
	
	NSNotificationCenter *notificationCenter = [NSNotificationCenter defaultCenter];
	//NSLog(@"%@", data);
	[notificationCenter postNotificationName:@"Got Twitter Pic" object:self 
																	userInfo:[NSDictionary dictionaryWithObjectsAndKeys:data, @"data", connectionID, @"id", nil]];
}
	


//=============================================================================================================================
#pragma mark SA_OAuthTwitterEngineDelegate
- (void) storeCachedTwitterOAuthData: (NSString *) data forUsername: (NSString *) username {
	NSUserDefaults			*defaults = [NSUserDefaults standardUserDefaults];
	
	[defaults setObject: data forKey: @"authData"];
	[defaults synchronize];
}

- (NSString *) cachedTwitterOAuthDataForUsername: (NSString *) username {
	return [[NSUserDefaults standardUserDefaults] objectForKey: @"authData"];
}

//=============================================================================================================================
#pragma mark SA_OAuthTwitterControllerDelegate
- (void) OAuthTwitterController: (SA_OAuthTwitterController *) controller authenticatedWithUsername: (NSString *) username {
	NSLog(@"Authenicated for %@", username);
}

- (void) OAuthTwitterControllerFailed: (SA_OAuthTwitterController *) controller {
	NSLog(@"Authentication Failed!");
}

- (void) OAuthTwitterControllerCanceled: (SA_OAuthTwitterController *) controller {
	NSLog(@"Authentication Canceled.");
}

- (void) authenticatedWithCookies: (NSArray *) cooks {
  NSLog(@"Authentication Success!");
  self.cookies = cooks;
  authenticated = YES;
	[(classiwhaleAppDelegate*)[UIApplication sharedApplication].delegate successfullyLoggedIn];
}

- (void) preapprovedWithCookies: (NSArray *) cooks {
  NSLog(@"Cookies Preapproved!");
  self.cookies = cooks;
  authenticated = YES;
}


//=============================================================================================================================
#pragma mark TwitterEngineDelegate
- (void) requestSucceeded: (NSString *) requestIdentifier {
	NSLog(@"Request %@ succeeded", requestIdentifier);
}

- (void) requestFailed: (NSString *) requestIdentifier withError: (NSError *) error {
	NSLog(@"Request %@ failed with error: %@", requestIdentifier, error);
}



// We don't want to allocate a new instance, so return the current one.
+ (id)allocWithZone:(NSZone*)zone {
	return [[self sharedInstance] retain];
}

// Equally, we don't want to generate multiple copies of the singleton.
- (id)copyWithZone:(NSZone *)zone {
	return self;
}

// Once again - do nothing, as we don't have a retain counter for this object.
- (id)retain {
	return self;
}

// Replace the retain counter so we can never release this object.
- (NSUInteger)retainCount {
	return NSUIntegerMax;
}

// This function is empty, as we don't want to let the user release this object.
- (void)release {
	
}

//Do nothing, other than return the shared instance - as this is expected from autorelease.
- (id)autorelease {
	return self;
}

@end
