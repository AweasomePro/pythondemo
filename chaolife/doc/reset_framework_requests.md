##要点
- 它继承HttpRequest,增加了灵活的REST 请求解析 和 认证
- Request object 提供了请求解析让你将requests当做一个JSON data  或者是其他的媒体类型
- .data 返回 request body的解析内容，这个 request.POST 和 request.FILES属性预期的一样，它包含了所有的请求内容（包括file 和 non-file）
另外，请求方式支持PUT、PATCH等，具体可以看 parses 的文档
- query_params 这个基本和 request.GET是一样，为了更好的表示你的代码，推荐使用 request.query_params，因为，如何http请求其实
都可以包含 params，不仅仅是GET fangshi
-parsers