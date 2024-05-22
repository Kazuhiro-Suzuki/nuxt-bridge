import '../import.dart';

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ちがさき障がい者支援アプリ',
      // theme: ThemeData(
      //   primarySwatch: Colors.blue,
      // ),
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: Colors.blue,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.blue,
        ),
        scaffoldBackgroundColor: Colors.blue.shade100,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}


class _MyHomePageState extends State<MyHomePage> {
  late WebViewController _webViewController;
  double _currentPositionX = 0;
  final Completer<WebViewController> _controller = Completer<WebViewController>();
  String? fcmToken;
  String? userAgent;
  FirebaseMessaging messaging = FirebaseMessaging.instance;

  @override
  void initState() {
    super.initState();
    NotificationApi.init(messaging);
    FirebaseMessaging.onMessage.listen((RemoteMessage message) async {
      print('received message from onMessage.');
      print(message.notification?.title);
      print(message.notification?.body);
      final notification = message.notification;
      final android = message.notification?.android;
      final apple = message.notification?.apple;
      if (notification != null && (android != null || apple != null)) {
        print("show LocalNotifications");
        NotificationApi.shownNotification(
          id: notification.hashCode,
          title: notification.title,
          body: notification.body,
        );
        // NotificationApi.shownNotification(
        //   title: 'title',
        //   body: 'Hey',
        // );
      }
    });

    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) async {
      print('received message from onMessageOpenedApp.');
    });
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
        onWillPop: () async {
          if (await _webViewController.canGoBack()) {
            print("-------goBack---------");
            _webViewController.goBack();
            return false;
          } else {
            return true;
          }
        },
        child: Scaffold(
          body: SafeArea(
            child: WebView(
                  // initialUrl: 'http://10.0.2.2:3000/home?citycode=142077',
                  // initialUrl: 'http://127.0.0.1:3000/home?citycode=142077',
                  // initialUrl: 'https://dev.lg-pwd.jp/home?citycode=142077',
                  // initialUrl: 'https://stg.lg-pwd.jp/home?citycode=142077',
                  initialUrl: 'https://lg-pwd.jp/home?citycode=142077',
                  javascriptMode: JavascriptMode.unrestricted,
                  userAgent: userAgent,
                  navigationDelegate: (NavigationRequest request) async {
                    switch(request.url){
                      case 'https://www.city.chigasaki.kanagawa.jp/otoshiyori/1023673.html':
                        launchURL('https://www.city.chigasaki.kanagawa.jp/otoshiyori/1023673.html');
                        return NavigationDecision.prevent;
                      case 'https://mirairoid.page.link/NLtk':
                        if (Platform.isAndroid) {
                          launchURL('https://lg-pwd.jp/mirairo?citycode=142077');
                          return NavigationDecision.prevent;
                        }
                        return NavigationDecision.navigate;
                      case 'https://www.city.chigasaki.kanagawa.jp/_res/projects/default_project/_page_/001/004/355/syuwa_shinsei20210401.pdf':
                        if (Platform.isAndroid) {
                          launchURL('https://www.city.chigasaki.kanagawa.jp/_res/projects/default_project/_page_/001/004/355/syuwa_shinsei20210401.pdf');
                          return NavigationDecision.prevent;
                        }
                        return NavigationDecision.navigate;
                      case 'https://d3n2js5ykzz1af.cloudfront.net/':
                        if (Platform.isAndroid) {
                            launchURL('https://d3n2js5ykzz1af.cloudfront.net/');
                            return NavigationDecision.prevent;
                        }
                        return NavigationDecision.navigate;
                      default:
                        return NavigationDecision.navigate;
                    }
                  },
                  onWebViewCreated: (WebViewController webViewController) async {
                    _webViewController = webViewController;
                    // _controller.complete(webViewController);
                    String _userAgent = await _webViewController.runJavascriptReturningResult("navigator.userAgent");
                    fcmToken = await getToken(messaging);
                    setState(() {
                      userAgent = '${_userAgent} Device-Token=${fcmToken}';
                      print("-----${fcmToken}-------onWebViewCreated------${userAgent}");
                    });
                  },
                ),
          ),
          bottomNavigationBar:  Platform.isIOS ? BottomAppBar(
              color: Colors.black,
              child:  IconTheme(
                data: const IconThemeData(color: Colors.white),
                child: Row(
                  children: <Widget>[
                    const Spacer(),
                    IconButton(
                      icon: const Icon(Icons.arrow_back_ios),
                      onPressed: () async {
                        if (await _webViewController.canGoBack()) {
                          _webViewController.goBack();
                        } 
                      },
                    ),
                    const Spacer(),
                    IconButton(
                      icon: const Icon(Icons.arrow_forward_ios),
                      onPressed: () async {
                        if (await _webViewController.canGoForward()) {
                          _webViewController.goForward();
                        } 
                      },
                    ),
                    const Spacer(flex: 5),
                    IconButton(
                      icon: const Icon(Icons.update),
                      onPressed: () async {
                        _webViewController.reload();
                      },
                    ),
                    const Spacer(),
                  ],
                ),
              ),
          ) : null,
        )
    );
  }
}