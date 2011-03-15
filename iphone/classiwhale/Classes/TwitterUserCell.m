//
//  TwitterUserCell.m
//  classiwhale
//
//  Created by Alex Churchill on 3/15/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import "TwitterUserCell.h"


@implementation TwitterUserCell

@synthesize user_name;
@synthesize screen_name;
@synthesize profileImage;
@synthesize act;

- (id)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier {
    if ((self = [super initWithStyle:style reuseIdentifier:reuseIdentifier])) {
        // Initialization code
    }
    return self;
}


- (void)setSelected:(BOOL)selected animated:(BOOL)animated {

    [super setSelected:selected animated:animated];

    // Configure the view for the selected state
}


- (void)dealloc {
    [super dealloc];
}


@end
