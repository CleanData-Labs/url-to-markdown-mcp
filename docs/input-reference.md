# Input reference: URL to Markdown for LLMs

Generated from the Actor's published input schema. All fields are optional unless marked required. The same fields are the arguments of the MCP tool `cleandata-labs--url-to-markdown`.

Live version: <https://apify.com/cleandata-labs/url-to-markdown/input-schema>

| Field | Type | Default | Description |
|---|---|---|---|
| `urls` **(required)** | array | `["https://en.wikipedia.org/wiki/Large_language_model", "https://docs.apify.com/platform/actors"]` | Public web pages or PDF links to convert, e.g. ["https://example.com/blog/post"]. 'https://' is added if missing. One converted page costs one result. Always pass your own URLs: the default list is only a demo. |
| `maxCrawlDepth` | integer (min 0, max 10) | `0` | How far to follow links on the same host, 0-10. 0 (default) = convert only the given URLs. 1 = also the pages they link to, 2 = one level more. Combine with maxPagesPerStartUrl to cap cost. |
| `useSitemap` | boolean | `false` | true = also find pages from the site's sitemap (robots.txt Sitemap entries or /sitemap.xml). Good for a whole docs site or blog. Cap it with maxPagesPerStartUrl. Default false. |
| `maxPagesPerStartUrl` | integer (min 0) | `50` | Max pages per start URL when crawling or using the sitemap, 0 = no limit. Default 50. Each page is charged, so keep it low (e.g. 5-20) for quick agent tasks. |
| `includeUrlGlobs` | array |  | Only crawl URLs that match one of these glob patterns, e.g. ["https://docs.example.com/guide/*"]. Used only when maxCrawlDepth > 0 or useSitemap is true. |
| `excludeUrlGlobs` | array |  | Skip URLs that match any of these glob patterns, e.g. ["*/tag/*", "*/page/*"]. |
| `extractionMode` | string: `auto` / `article` / `full` | `"auto"` | How much of each page to keep: "auto" (default) = main content, falling back to the full page if too little text is found; "article" = main content only; "full" = whole page including navigation, header and footer. |
| `outputFormats` | array of `markdown` / `text` / `html` | `["markdown"]` | One or more of "markdown" (default), "text" (plain text) and "html" (cleaned HTML of the main content). Ask only for what you need: every extra format makes the output larger. |
| `removeElementsCssSelector` | string |  | Optional CSS selector of elements to delete before extraction, e.g. ".newsletter, .related-posts, #comments". |
| `keepElementsCssSelector` | string |  | Optional CSS selector: if set, only these elements are converted, e.g. "article" or ".docs-content". |
| `includeLinkList` | boolean | `false` | true = also return lists of internal and external links found on each page. Default false. |
| `maxPdfPages` | integer (min 0) | `50` | PDF links are converted to text automatically. Max pages read per PDF, 0 = all. Default 50. |
| `renderJs` | string: `auto` / `never` / `always` | `"auto"` | When to use a headless browser: "auto" (default) = only when the plain HTTP result is too thin; "never" = fastest; "always" = for JavaScript-heavy single-page apps. |
| `waitForSelector` | string |  | Optional CSS selector to wait for before reading the page when the browser is used, e.g. "main article". |
| `dynamicContentWaitSecs` | integer (min 0, max 30) | `0` | Extra seconds to wait after page load when the browser is used, 0-30. Default 0. |
| `includeLinks` | boolean | `true` | true (default) = keep hyperlinks as Markdown links with absolute URLs. false = plain text only, which saves tokens. |
| `includeImages` | boolean | `false` | true = keep images as Markdown image tags. Default false. |
| `includeTables` | boolean | `true` | true (default) = convert HTML tables to Markdown tables. |
| `chunkSizeTokens` | integer (min 0, max 32000) | `0` | If > 0, also return 'chunks' split on paragraph boundaries for RAG, about this many tokens each (1 token ~ 4 characters), max 32000. Default 0 = no chunks. |
| `chunkOverlapTokens` | integer (min 0, max 2000) | `50` | Overlap between consecutive chunks in tokens, 0-2000. Default 50. Used only when chunkSizeTokens > 0. |
| `maxCharacters` | integer (min 0) | `0` | Cut each page's Markdown to this many characters, 0 = no limit (default). For AI agents a value such as 20000 (~5k tokens) keeps results small enough to read in one step. |
| `respectRobotsTxt` | boolean | `true` | true (default) = skip URLs that the site's robots.txt disallows. Skipped URLs are reported and not charged. |
| `minContentCharsBeforeBrowserFallback` | integer | `400` | In renderJs=auto, use the browser if plain HTTP extraction returns fewer characters than this. Default 400. |
| `requestTimeoutSecs` | integer (min 5, max 120) | `30` | Timeout per attempt in seconds, 5-120. Default 30. |
| `maxRetries` | integer (min 0, max 5) | `2` | Retries per URL on network errors, HTTP 429 and 5xx, 0-5. Default 2. |
| `maxConcurrency` | integer (min 1, max 20) | `8` | Parallel HTTP requests, 1-20. Default 8. |
| `proxyConfiguration` | object | `{"useApifyProxy": false}` | Optional proxy for sites that block datacenter IPs, e.g. {"useApifyProxy": true}. Default: no proxy. |
| `userAgent` | string |  | Optional custom User-Agent header. By default the Actor uses an identifiable bot User-Agent. |
| `customHttpHeaders` | object |  | Optional extra HTTP headers, e.g. {"Accept-Language": "de-DE"}. Do not put credentials for sites you are not authorized to access. |
