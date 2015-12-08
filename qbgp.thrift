
struct Update {
    1: i32 type,
    2: i32 reserved,
    3: i32 prefixlen,
    4: i32 label,
    5: string rd,
    6: string prefix,
    7: string nexthop
}

struct Routes {
    1: i32 errcode,
    2: optional list<Update> updates,
    4: optional i32 more
}

service BgpConfigurator {
    i32 startBgpServer(1:i32 asNumber, 2:string routerId, 3: i32 port, 
                       4:i32 holdTime, 5:i32 keepAliveTime),
    i32 stopBgpServer(),
    i32 createPeer(1:string neighborIpAddress, 2:i32 asNumber),
    i32 deletePeer(1:string neighborIpAddress),
    i32 addRouteMapToMPBGPPeer(1:string neighborIpAddress, 2:i32 routeMapNumber),
    i32 deleteRouteMapToMPBGPPeer(1:string neighborIpAddress, 2:i32 routeMapNumber),
    i32 addVrf(1:string rd, 2:list<string> irts, 3:list<string> erts),
    i32 delVrf(1:string rd),
    i32 pushRoute(1:i32 aclNum, 2:i32 routeMapNum, 3:i32 seqNum, 4:string prefix, 5:string wildcard, 6:string neighborIpAddress, 7:i32 vpnNum),
    i32 withdrawRoute(1:i32 aclNum, 2:i32 routeMapNum, 3:i32 seqNum, 4:string prefix, 5:string neighborIpAddress),
    Routes getRoutes(1:i32 optype, 2:i32 winSize),
    string getRouteTarget(1:string prefix)
}

service BgpUpdater {
    oneway void onUpdatePushRoute(1:string rd, 2:string prefix, 
                                  3:i32 prefixlen, 4:string nexthop, 
                                  5:i32 label),
    oneway void onUpdateWithdrawRoute(1:string rd, 2:string prefix, 
                                      3:i32 prefixlen), 
    oneway void onStartConfigResyncNotification()
}
    

