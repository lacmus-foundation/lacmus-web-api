using System.Text.Json.Serialization;

namespace Identity.ViewModels.Token
{
    public class RefreshToken
    {
        [JsonPropertyName("access_token")]
        public string Token { get; set; }
    }
}