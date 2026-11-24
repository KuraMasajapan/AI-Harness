# AIによる自宅Wi-Fi診断・速度3倍というX投稿の調査

- Date: 2026-11-24
- Source: https://x.com/franpradasAI/status/2124931492518449500
- Source status: Weirで親投稿と本人の続きスレッドを実際に取得
- Stage 1 rank: B
- Stage 2 rank: B（手法の技術的妥当性は部分確認、3倍という効果の因果関係・再現性は未確認）
- Evidence: CONFIRMED（投稿内容・チャネル幅、NETGEAR仕様など一般仕様）、UNVERIFIED（実施者の測定・改善率・効果内訳）
- Disposition: HOLD（AI-Harness Coreへの採用不要。再現可能な診断チェックリストとして候補保持）
- Status: KNOWLEDGE / RESEARCH-ONLY / NOT IMPLEMENTED
- Authorization: B以上の研究保存に関するHuman継続指示。外部ネットワーク設定変更や実装は行わない。

## 投稿原文の要点（スペイン語Xスレッド）

- 投稿者Fran Pradasは、「ルーターを交換せずAIに診断させてWi-Fi速度が216Mbpsから669Mbpsへ（約3.10倍）、遅延39%減」と紹介。
- Codex、Claude Code、Claude Cowork等のPCを利用できるAIを想定。Macの `networkQuality -v` を紹介しWindowsは別ツールで代替。
- プロンプトの調査手順：(1) Wi-Fi帯域/チャネル/チャネル幅/信号・ノイズ・誤り/周辺ネットワーク走査、(2) ルータと1.1.1.1へ30パケットping、および5 hop traceroute、(3) ルータDNS、1.1.1.1、8.8.8.8の応答時間比較、(4) networkQuality -vによる測定、(5) 影響度順に課題を整理しルータ型番を確認、変更後同条件で再テスト。
- ケースのルータはNETGEAR CAX30、周辺52ネットワークと主張。5GHz帯で40→80MHz、Wi-Fi 6有効化、チャネル36→48、2.4GHzは9→11、2.4/5GHz SSIDを分離、Cloudflare DNS優先化。
- 投稿者によれば、AIは計測・提案・PC DNS変更を担当し、ルータ設定は人が手動実施。
- 親投稿・関連スレッド： https://x.com/franpradasAI/status/2124931504870760791 ; https://x.com/franpradasAI/status/2124931516577055115 ; https://x.com/franpradasAI/status/2124931528388137205 ; https://x.com/franpradasAI/status/2124931540203508127 ; https://x.com/franpradasAI/status/2124931552065007748

## 第2段階：技術検証

- NETGEARメーカー仕様CAX30の5GHzは80MHz、Wi-Fi 6 (802.11ax) 対応。216→669Mbpsの絶対値は機器性能から見て不自然ではない。
- 5GHz幅40→80MHzは理論的リンク速度を上げ得るが、周辺Wi-Fiが多い場合、干渉範囲が広がり、実効速度/安定性の改善は保証されない（Intel、Cisco、Aruba）。幅変更、Wi-Fi 6有効化、周辺負荷の時間変動が重なるため因果分離不能。
- 5GHzの20MHzチャネル36・40・44・48は同一80MHzチャネルブロック。36→48だけで別の空き80MHz帯へ移動したとみなすのは誤り。Primaryチャネル変更の効果はあり得るが帯域全体の回避ではない。
- 2.4GHzのチャネル1/6/11（20MHz）は重複の少ない代表的選択。9→11は合理性あり、ただし周辺環境依存。
- DNS変更はドメイン名解決の遅延を改善し得るが、通常ダウンロード回線帯域の向上要因ではない。
- networkQualityはインターネット経路を含む容量・応答性測定であり純粋なWi-Fiリンク速度計測ではない。時間帯、測定サーバー、電波環境、WAN混雑、機器の位置、端末数が結果に影響。
- 変更前後の再現性ある複数回測定、ログ、ルータ設定画面、制御されたA/B実験は未確認。3.1倍という改善を一般化しない。

## AI-Harnessへの有用性

ネットワーク診断作業をエージェントで手順化する知識としてはB。OSS新規実装、AIエージェント構築方法、新たなAPIやHarness Core機能に当たらず、重複の可能性が高い一般的診断手法。自宅/仕事の接続問題やDNS調査を行う際に呼び出す読み取り中心の診断チェックリストへ限定。ルータ変更、ネットワーク構成書換え、DNS変更はHuman確認後にのみ実施。

## 安全な検証順

1. Wi-Fiか有線か、ルーター型番、端末OS、ISP契約、通信方式を確認。
2. 同じ端末・場所・日時条件で数回の速度測定、Wi-Fiリンク速度とWAN速度を区別。
3. 端末の信号強度、チャネル、5GHz/2.4GHz、接続規格、周辺APの混雑を読み取りだけで記録。パスワードやSSID等のプライベート情報を外部送信しない。
4. ping/traceroute/DNS照会を個別・直列に実行。ネットワーク負荷を避ける。
5. 改善案の想定効果・副作用とロールバック手順を提示しHuman承認を取る。
6. 変更は一項目ずつ行い、複数回計測・比較する。繋がらなくなる恐れのある設定には復旧手順が必須。

## 参照資料

- https://www.netgear.com/media/cax30_ds_22mar21_tcm148-120996.pdf
- https://www.intel.com/content/www/us/en/support/articles/000058989/wireless/intel-killer-wi-fi-products.html
- https://arubanetworking.hpe.com/techdocs/ArubaOS/AOS_8x_WebHelp/Content/arubaos-solutions/access-points/chan-grop-scan.htm
- https://www.tp-link.com/us/support/faq/4309/
- https://man.freebsd.org/cgi/man.cgi?manpath=macOS+26.7&query=networkQuality&sektion=8

## Recall triggers

AIでWi-Fi改善、WiFi最適化、216→669Mbps、ネットワーク診断、Codex、networkQuality、チャンネル36/48、80MHz、DNS、ルーター、Fran Pradas
