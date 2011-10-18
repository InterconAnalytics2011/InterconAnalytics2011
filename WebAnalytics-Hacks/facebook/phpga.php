<?php
class GoogleAnlayticsMobile {
	private $__utma; 						// Google Analytics __utma cookie
	private $__utma_c_time = 63072000; 		// 2 years (2 years is the default in Google Analytics)
	private $__utmb; 						// Google Analytics __utmb cookie
	private $__utmb_c_time = 1800; 			// 30 minutes (30 minutes is the default in Google Analytics)
	private $__utmc;						// Google Analytics __utmc cookie
	private $__utmz;						// Google Analytics __utmz cookie
	private $__utmz_c_time = 604800; 		// 7 days (6 months is the default in Google Analytics)
	private $ga_utmhn;						// Site host
	private $ga_utmac;						// Google Analytics account
	private $ga_utmwv = "4.3.1";			// Google Analytics tracking code version
	private $ga_hash;						// Google Analytics hash for domain
	private $ga_img = "http://www.google-analytics.com/__utm.gif";
	private $ga_search = array(array("google","q"),array("yahoo","p"),array("msn","q"),array("bing","q"),array("aol","query"),array("aol","encquery"),array("lycos","query"),array("ask","q"),array("altavista","q"),array("netscape","query"),array("cnn","query"),array("looksmart","qt"),array("about","terms"),array("mamma","query"),array("alltheweb","q"),array("gigablast","q"),array("voila","rdata"),array("virgilio","qs"),array("live","q"),array("baidu","wd"),array("alice","qs"),array("yandex","text"),array("najdi","q"),array("aol","q"),array("club-internet","query"),array("mama","query"),array("seznam","q"),array("search","q"),array("wp","szukaj"),array("onet","qt"),array("netsprint","q"),array("google.interia","q"),array("szukacz","q"),array("yam","k"),array("pchome","q"),array("kvasir","searchExpr"),array("sesam","q"),array("ozu","q"),array("terra","query"),array("nostrum","query"),array("mynet","q"),array("ekolay","q"),array("search.ilse","search_for"));
	private $ga_referer;
	private $time;
	private $html;
 
	function __construct($ga_utmac, $ga_utmhn, $URI = NULL, $ga_params = array()) {
		$this->ga_utmac = $ga_utmac;
		$this->ga_utmhn = preg_replace('/^./','',$ga_utmhn); //changed by Yamada
		$this->ga_hash = $this->Hash($ga_utmhn);
 
		// Set the time for the request
		$this->time = time();
		// Set the page URI that is request
		if($URI==NULL) $URI = $_SERVER['REQUEST_URI'];
		// Set the referer page
		$this->ga_referer = $_SERVER['HTTP_REFERER'];
		// Set the visitor source
		$source = $this->GetTrafficSource();
		// Set the new traffic source
		if($source["utmgclid"]!="") $source_str = "utmgclid=".$source["utmgclid"];
		else $source_str = "utmcsr=".$source["utmcsr"];
		$source_str .= "|utmccn=".$source["utmccn"]."|utmcmd=".$source["utmcmd"];
		if($source["utmctr"]!="") $source_str .= "|utmctr=".$source["utmctr"];
		if($source["utmcct"]!="") $source_str .= "|utmcct=".$source["utmcct"];
 
		// Set all extra parameters like screen resolution, color depth
		if(is_array($ga_params)) foreach ($ga_params as $key => $value) $ga_set_params .= "&".$key."=".rawurlencode($value);
		else $ga_set_params = "";
 
		// Check if Google Analytics cookie "__utma" already exists
		if(isset($_COOKIE["__utma"])) {
			// Save cookies to local variable
			$this->__utma = $_COOKIE["__utma"];
			$this->__utmb = $_COOKIE["__utmb"];
			$this->__utmz = $_COOKIE["__utmz"];
 
			$__utmb = split("\.",$this->__utmb);
 
			if(strpos($this->__utmz,"utmgclid")>-1) $pos = strpos($this->__utmz,"utmgclid");
			else $pos = strpos($this->__utmz,"utmcsr");
			$__utmz = split("\.",substr($this->__utmz,0,$pos));
			$__utmz[4] = substr($this->__utmz,$pos);
			$__utma = split("\.",$this->__utma);
 
			// Check if Google Analytics "session" cookie "__utmc" exists, if not create one and update the number of visits in cookie: "__utma"
			if(!isset($_COOKIE["__utmc"])) {
				// Increase the number of visits
				$__utma[5] = $__utma[5]+1;
				// Update the time of the visit
				$__utma[3] = $__utma[4];
				$__utma[4] = $this->time;
				// Save cookies
				$this->__utma = join(".",$__utma);
				setcookie("__utma", $this->__utma, $this->time+$this->__utma_c_time, "/", ".".$this->ga_utmhn);
				setcookie("__utmc", $__utma[0], 0, "/", ".".$this->ga_utmhn);
				// Update "__utmb" cookie with the number of pageviews or create a new cookie
				if(isset($_COOKIE["__utmb"])) $__utmb[1] = 1;
				else $__utmb = array($__utma[0], 1, 10, $this->time);
			}
			else $__utmb[1] = $__utmb[1]+1; // Increase the number of pageviews in "__utmb" cookie
 
			// Update the traffic source
			if($__utmz[4]!=$source_str && $source["utmcsr"]!="(direct)") $__utmz = array($__utmz[0], $this->time, $__utma[5], $__utmz[3]+1, $source_str);
 
			// Save cookies "__utmb" and "__utmz"
			$this->__utmb = join(".",$__utmb);
			setcookie("__utmb", $this->__utmb, $this->time+$this->__utmb_c_time, "/", ".".$this->ga_utmhn);
			$this->__utmz = join(".",$__utmz);
			setcookie("__utmz", $this->__utmz, $this->time+$this->__utmz_c_time, "/", ".".$this->ga_utmhn);
		}
		else {
			// No Google Analytics cookies exists, create new ones and save them i local variables
			$c_id = sprintf("%f", (rand(1000000000,2147483647) ^ $this->ga_hash) * 2147483647);
			$c_id = split("\.",$c_id);
			$this->__utma = $this->ga_hash.".".$c_id[0].".".$this->time.".".$this->time.".".$this->time.".1";
			$this->__utmb = $this->ga_hash.".1.10.".$this->time;
			$this->__utmc = $this->ga_hash;
			$this->__utmz = $this->ga_hash.".".$this->time.".1.1.".$source_str;
			setcookie("__utma", $this->__utma, $this->time+$this->__utma_c_time, "/", ".".$this->ga_utmhn);
			setcookie("__utmb", $this->__utmb, $this->time+$this->__utmb_c_time, "/", ".".$this->ga_utmhn);
			setcookie("__utmc", $this->__utmc, 0, "/", ".".$this->ga_utmhn);
			setcookie("__utmz", $this->__utmz, $this->time+$this->__utmz_c_time, "/", ".".$this->ga_utmhn);
		}
		// Create the pageview request to Google Analytics image
		$this->html .= "<img src=\"".$this->ga_img."?utmwv=".$this->ga_utmwv."&utmn=".rand(1000000000,9999999999)."&utmhn=".$this->ga_utmhn."".$ga_set_params."&utmhid=".rand(1000000000,9999999999)."&utmr=".rawurlencode($this->ga_referer)."&utmp=".rawurlencode($URI)."&utmac=".$this->ga_utmac."&utmcc=__utma%3D".$this->__utma."%3B%2B__utmz%3D".rawurlencode($this->__utmz)."%3B\" width=\"1\" height=\"1\" />\n";
	}
 
	function Hash($d) {
	
		if(!$d || $d=="") return 1;
		$h=0; $g=0;
		for($i=strlen($d)-1;$i>=0;$i--) {
			$c = (int)(ord($d[$i]));
			$h = (($h << 6) & 0xfffffff) + $c + ($c << 14);
			$g = ($h & 0xfe00000);
			if($g!=0) $h = ($h ^ ($g >> 21));
		}
		
		return $h;
	}
 
	function GetTrafficSource() {
		if(isset($_GET["gclid"])){
			return array("utmgclid"=>$_GET["gclid"], "utmcsr"=>"", "utmccn"=>"(none)", "utmcmd"=>"(none)", "utmctr"=>"", "utmcct"=>"");
		}
		else if(isset($_GET["utm_source"]) && isset($_GET["utm_medium"])) { 
			// The traffic source i set in the URL
			$utmccn = isset($_GET["utm_campaign"]) ? $_GET["utm_campaign"] : "(not set)";
			$utmcct = isset($_GET["utm_content"]) ? $_GET["utm_content"] : "(not set)";
			return array("utmgclid"=>"", "utmcsr"=>$_GET["utm_source"], "utmccn"=>$utmccn, "utmcmd"=>$_GET["utm_medium"], "utmctr"=>$_GET["utm_term"], "utmcct"=>$utmcct);
		}
		else if($this->ga_referer!="") { 
			// The treffic source is from a referral site
			$search_engine = $this->GetSearchEngine();
			// Check if it's a search engine
			if($search_engine) return $search_engine; 
			else if(!isset($_COOKIE["__utmc"])) { 
				// It's not a search engine and it's a new visit. Set the referer.
				$ref = $this->GetReferer();
				if(substr($ref["host"],0,4)=="www.") $ref["host"] = substr($ref["host"],4); // Remove www from URL
				return array("utmgclid"=>"", "utmcsr"=>$ref["host"], "utmccn"=>"(referral)", "utmcmd"=>"referral", "utmctr"=>"", "utmcct"=>$ref["uri"]);
			}
		}
		return array("utmgclid"=>"", "utmcsr"=>"(direct)", "utmccn"=>"(direct)", "utmcmd"=>"(none)", "utmctr"=>"", "utmcct"=>"");
	}
 
	function GetSearchEngine() {
		$ref = $this->GetReferer();
		for($ii=0;$ii<count($this->ga_search);$ii++) {
			if(strpos(strtolower($ref["host"]), strtolower($this->ga_search[$ii][0]))>-1) {
				$test1 = strpos($ref["referer"], "?".$this->ga_search[$ii][1]."=");
				$test2 = strpos($ref["referer"], "&".$this->ga_search[$ii][1]."=");
				$i = ($test1 > -1) ? $test1 : $test2;
				if($i>-1) {
					$k = substr($ref["referer"], $i+strlen($this->ga_search[$ii][1])+2, strlen($ref["referer"]));
					$i = strpos($k,"&");
					if($i > -1) $k = substr($k,0,$i);
					if(isset($_GET["gclid"])) return array("utmgclid"=>$_GET["gclid"], "utmcsr"=>"", "utmccn"=>"(not set)", "utmcmd"=>"(not set)", "utmctr"=>$k, "utmcct"=>"");
					else return array("utmgclid"=>"", "utmcsr"=>$this->ga_search[$ii][0], "utmccn"=>"(organic)", "utmcmd"=>"organic", "utmctr"=>$k, "utmcct"=>"");
				}
			}
		}
		return false;
	}
 
	function GetReferer() {
		$referer_tmp = $this->ga_referer;
		$pos = strpos($referer_tmp, "://");
		if($pos>0) $referer_tmp = $referer_tmp = substr($referer_tmp,$pos+3);
		$pos = strpos($referer_tmp, "/");
		if($pos>0) return array("host"=>substr($referer_tmp, 0, $pos), "uri"=>substr($referer_tmp, $pos), "referer"=>$this->ga_referer);
		else return array("host"=>$referer_tmp, "uri"=>"", "referer"=>$this->ga_referer);
	}
 
	function SetTransaction($order_id, $amount, $shipping, $tax, $city, $region, $country) {
		// Generate code to set a new transaction in Google Analytics
		$this->html .= "<img src=\"".$this->ga_img."?utmwv=".$this->ga_utmwv."&utmn=".rand(1000000000,9999999999)."&utmhn=".$this->ga_utmhn."&utmt=tran&utmtid=".$order_id."&utmtto=".$amount."&utmttx=".$tax."&utmtsp=".$shipping."&utmtci=".rawurlencode($city)."&utmtrg=".rawurlencode($region)."&utmtco=".rawurlencode($country)."&utmac=".$this->ga_utmac."&utmcc=__utma%3D".$this->__utma."%3B%2B__utmz%3D".rawurlencode($this->__utmz)."%3B\" width=\"1\" height=\"1\" />\n";
	}
 
	function SetTransactionItem($order_id, $item_id, $category, $name, $price, $quantity) {
		// Generate code to set a new transaction item in Google Analytics, you must call the function SetTransaction before you call this one.
		$this->html .= "<img src=\"".$this->ga_img."?utmwv=".$this->ga_utmwv."&utmn=".rand(1000000000,9999999999)."&utmhn=".$this->ga_utmhn."&utmt=item&utmtid=".$order_id."&utmipc=".$item_id."&utmipn=".rawurlencode($name)."&utmiva=".rawurlencode($category)."&utmipr=".$price."&utmiqt=".$quantity."&utmac=".$this->ga_utmac."&utmcc=__utma%3D".$this->__utma."%3B%2B__utmz%3D".rawurlencode($this->__utmz)."%3B\" width=\"1\" height=\"1\" />\n";
	}
 
	function GetTrackingCode() {
		// Return the Google Analytics code for this request
		return $this->html;
	}
}
 
 
//$ga_params = array();
//$ga_params["utmsr"] = $properties["displayWidth"]."x".$properties["displayHeight"];
//$ga_params["utmsc"] = $properties["displayColorDepth"]."-bit";
 
//$ga = new GoogleAnlayticsMobile("UA-11569960-8", ".sslblindado.com", NULL, $ga_params);

//$ga->SetTransaction("1234", 219, 29, 0, "Stockholm", "", "Sweden");
//$ga->SetTransactionItem("1234", "PR1", "", "Product 1", 190, 1);
//$ga->SetTransactionItem("1234", "SH1", "", "Shipping 1", 29, 1);
?>

