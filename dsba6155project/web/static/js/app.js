
// var app = (function(){
//
//   return {
//     nextPage: function(url , selector){
//       console.log(selector)
//       $(selector).css("iframe").remove();
//       $("<iframe/>" , {"href" : url}).appendTo(selector)
//
//       //$( selector).append( ifr );
//     }
//   }
// })()


var appVue = new Vue({
        el: '#app',
        data: function(){

            return {
              currentPage: 0
            }
        },
        methods: {
          _loadPage: function(){
            $("#viewbox").load("/page/"+this.currentPage +"/")
          },
          nextPage: function(){
                this.currentPage += 1;
                this._loadPage()
          },
          previousPage: function(){
            this.currentPage -= 1;
            if(this.currentPage == 0){
              window.location = "/"
            }
            else{
              this._loadPage()
            }

          },
          getCurrentPage: function(){
            if(this.currentPage == 0)return "";
            else return "/page/"+this.currentPage + "/"
          }
        }
})
